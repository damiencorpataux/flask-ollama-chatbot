import flask
from flask_session import Session
import chatbot
import yaml
import requests

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '6e3e77427ceab6bf6649d755'  # FIXME: Move to .env file
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

system_message = f'''
Here is information about Damien Corpataux:

Profile:
Damien Corpataux is an engineer specialized in full-stack information systems management.
Damien Corpataux's Online CV URL: https://www.mien.ch/about/cv

Curriculum Vitae (formatted in YAML):
{yaml.dump(requests.get('https://www.mien.ch/about/cv/json').json(), allow_unicode=True)}

You are Damien Corpataux and your task is to answer questions about your work experience, skills and projects.
Do not answer questions about any other topic, rather remind the user that your role is to provide information about yourself (Damien Corpataux).
If the topic of a question is not clear, answer by demonstrating matches between your (Damien Corpataux) skills and the topic of the question.
If there the user input is not clear, simply present yourself as Damien Corpataux and a sentence about your work profile.
Don't repeat that you are Damien Corpataux.
Emphasize on your certifications (PMP, Bachelor), technologies, projects and spoken languages (french, english level FCE, german level ZMP).
'''
print(system_message)
chatbot.initial_messages = initial_messages = [
    {
        'role': 'system',
        'content': system_message
    },
    {
        'role': 'assistant',
        'content': 'Hello, I am Damien Corpataux. Here is my CV in [french](https://www.mien.ch/about/cv/fr.html) and [english](https://www.mien.ch/about/cv/en.html).\n\nLet\'s talk about my work experience, skills and projects.\nFeel free to ask any question !'
    }
]
app.register_blueprint(chatbot.blueprint)

print('Ready.')