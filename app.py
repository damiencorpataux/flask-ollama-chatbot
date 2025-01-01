import flask
from flask_session import Session
import chatbot
import markdownify
import requests

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '6e3e77427ceab6bf6649d755'  # FIXME: Move to .env file
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

system_message = f'''
Here is information about Damien Corpataux:

[[Profile]]
Damien Corpataux is an engineer specialized in full-stack information systems management.
[[/Profile]]

[[Curriculum-vitae]]
${markdownify.markdownify(requests.get('https://www.mien.ch/about/cv').text, heading_style="ATX")}
[[/Curriculum-vitae]]

[[Work-projects]]
${markdownify.markdownify(requests.get('https://www.mien.ch/about/projects').text, heading_style="ATX")}
[[/Work-projects]]

Your mission is to answer questions about Damien Corpataux.
Do not answer questions about any other topic, rather remind the user that your role is to provide information about Damien Corpataux.
If the topic of a question is not clear, keep the focus on Damien Corpataux.
'''
print(system_message)
chatbot.initial_messages = initial_messages = [
    {
        'role': 'system',
        'content': system_message
    },
    {
        'role': 'assistant',
        'content': 'Hello, I am here to talk about Damien Corpataux. Feel free to ask any question !'
    }
]
app.register_blueprint(chatbot.blueprint)

print('Ready.')