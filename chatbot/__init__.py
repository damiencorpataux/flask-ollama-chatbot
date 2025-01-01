import ollama
import flask

blueprint = flask.Blueprint(
    'chatbot',
    __name__,
    template_folder='templates')

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
def api_chat_say(question):
    flask.session['messages'].append({'role': 'user', 'content': question})
    response = ollama.chat(
        model=model,
        messages=flask.session['messages'],
        # stream=True,
        options={
            'max_tokens': 2048
        }
    )
    # def generate():
    #     for chunk in response:
    #         print(chunk['message']['content'], end='', flush=True)
    #         flask.session['messages'][-1]['content'] += chunk['message']['content']
    #         yield chunk['message']['content']
    #     print('DONE !!!!!!!!!!!!!!!!!', flask.session['messages'][-1])
    # return flask.stream_with_context(generate())
    flask.session['messages'].append({'role': 'assistant', 'content': response['message']['content']})
    return response['message']['content']

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
