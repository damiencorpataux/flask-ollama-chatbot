import ollama
import flask
from flask_session import Session

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '6e3e77427ceab6bf6649d755'  # FIXME: Move to .env file
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

model = 'llama3.2'

@app.before_request
def before_request():
    try:
        flask.session['messages']
    except KeyError:
        flask.session['messages'] = [
            {
                'role': 'system',
                'content': 'Your mission is to answer questions about Damien Corpataux. Do not answer questions about any other topic. '
            }
        ]
        print('Initialized chat messages:', flask.session['messages'])

@app.route('/')
def web_ui():
    return flask.render_template('home.html')

@app.route('/chat/say/<path:question>')
def api_chat_say(question):
    flask.session['messages'].append({'role': 'user', 'content': question})
    response = ollama.chat(
        model=model,
        messages=flask.session['messages'],
        # stream=True,
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

@app.route('/chat/history')
def api_chat_history():
    messages = list(filter(
        lambda m: m.get('role') in ['user', 'assistant'],
        flask.session['messages']))
    return flask.jsonify(messages)

@app.route('/chat/clear')
def api_chat_clear():
    del flask.session['messages']
    before_request()
    return '', 201