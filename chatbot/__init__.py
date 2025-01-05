import ollama
import flask
import flask_limiter
import requests
import uuid
from collections import defaultdict

blueprint = flask.Blueprint(
    'chatbot',
    __name__,
    template_folder='templates')

limiter =flask_limiter.Limiter(
    flask_limiter.util.get_remote_address,
    app=flask.current_app,
    # default_limits=["100 per minute"],
    storage_uri="memory://",
)

model = 'llama3.2'
languages = ['en', 'fr']
system_message = 'You are a helpful assistant.'
first_message = 'Hello, how can I help you ?'
messages_dirty = defaultdict(list)  # A per session.uid dict of messages written to session (not saved because of streaming)

@blueprint.before_request
def before_request():
    initial_messages = [
        {
            'role': 'system',
            'content': system_message
        },
        {
            'role': 'assistant',
            'content': first_message
        }
    ]
    # Setup session uid
    try:
        flask.session['uid']
    except KeyError:
        flask.session['uid'] = uuid.uuid4()
    # Setup initial messages
    try:
        flask.session['messages']
    except KeyError:
        flask.session['messages'] = initial_messages
        print('Initialized chat messages:', flask.session['messages'])
    # Add dirty messages (not yet written to session) to actual session
    flask.session['messages'] += messages_dirty[flask.session['uid']]
    del messages_dirty[flask.session['uid']]

@blueprint.route('/')
@blueprint.route('/<lang>')
def web_ui(lang='en'):
    api_chat_translate(lang)  # FIXME: Pageload too long, make it async
    return flask.render_template('home.html', languages=languages)

@blueprint.route('/chat/say/<path:question>')
@limiter.limit("10 per minute")
def api_chat_say(question):
    flask.session['messages'].append({'role': 'user', 'content': question})
    answer = ollama.chat(
        model=model,
        messages=flask.session['messages'],
        options={
            'max_tokens': 32768
        },
        stream=True
    )
    # flask.session['messages'].append({'role': 'assistant', 'content': answer['message']['content']})
    # return answer['message']['content']
    # FIXME: Returning streamed answer prevent from writing to session,
    #   due to the http headers already sent.
    def generate():
        messages_dirty[flask.session['uid']].append({'role': 'assistant', 'content': ''})
        for chunk in answer:
            # print(chunk['message']['content'], end='', flush=True)
            messages_dirty[flask.session['uid']][-1]['content'] += chunk['message']['content']
            yield chunk['message']['content']
        print(messages_dirty[flask.session['uid']])
    return flask.stream_with_context(generate())

@blueprint.route('/chat/history')
def api_chat_history():
    messages = list(filter(
        lambda m: m.get('role') in ['user', 'assistant'],
        flask.session['messages']))
    return flask.jsonify(messages)

@blueprint.route('/chat/clear')
def api_chat_clear():
    del flask.session['messages']
    before_request()
    return '', 201

# @blueprint.route('/chat/translate')
def api_chat_translate(lang):
    # FIXME: make it called async'ly from the webpage.
    if lang != flask.session.get('last_translated_to'):
        if lang == 'en':
            translation = first_message
        else:
            translation = translate('en', lang, flask.session['messages'][1]['content'])
        flask.session['messages'][1]['content'] = translation
        flask.session['last_translated_to'] = lang

def translate(source, destination, text):
    import random
    response = requests.get(
        'https://translate.google.so/translate_a/t',
        params={
            'q': text,
            'tl': destination,
            'sl': 'auto',
            'client': hex(random.getrandbits(128))[2:],
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'tbb': 1
    })
    if response.ok:
        return response.json()[0][0]
    else:
        return f'Could not translate text ({response.status_code})\n\n{text}'
        # raise RuntimeError('Could not translate:', response.text)
    # response = ollama.chat(
    #     model=model,
    #     messages=[
    #         {
    #             'role': 'system',
    #             'content': f'You are a language translator. Please translate the user input from {source} to {destination} without any comment or remark. Just output the translated text. Use a very polite and inviting tone.'
    #         },
    #         {
    #             'role': 'user',
    #             'content': text
    #         }
    #     ],
    #     options={
    #         # 'max_tokens': 32768
    #     }
    # )
    # return response['message']['content']
