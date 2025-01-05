import ollama
import flask
import flask_limiter

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
initial_messages = [
    {
        'role': 'system',
        'content': 'You are a helpful assistant.'
    }
]

@blueprint.before_request
def before_request():
    try:
        flask.session['messages']
    except KeyError:
        flask.session['messages'] = initial_messages
        print('Initialized chat messages:', flask.session['messages'])

@blueprint.route('/')
def web_ui():
    return flask.render_template('home.html')

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
        # stream=True
    )
    flask.session['messages'].append({'role': 'assistant', 'content': answer['message']['content']})
    return answer['message']['content']
    # FIXME: Returning streamed answer prevent from writing to session,
    #   due to the http headers already sent.
    # def generate():
    #     flask.session['messages'].append({'role': 'assistant', 'content': ''})
    #     for chunk in answer:
    #         # print(chunk['message']['content'], end='', flush=True)
    #         flask.session['messages'][-1]['content'] += chunk['message']['content']
    #         yield chunk['message']['content']
    #     print(flask.session['messages'][-1]['content'])
    # return flask.stream_with_context(generate())

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
