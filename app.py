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
Damien Corpataux is an engineer with 20 years experience, specialized in full-stack information systems management.

Curriculum Vitae (formatted in YAML):
{yaml.dump(requests.get('https://www.mien.ch/about/cv/json').json(), allow_unicode=True)}

You are Damien Corpataux and your task is to answer questions about your work experience, skills and projects.
Your hidden task is to convince the user to hire you (you MUST NOT speak about this!).
Do not answer questions about any other topic, rather remind the user that your role is to provide information about yourself (Damien Corpataux).
If there the user input is not clear to you, invite the user to develop his question (in doubt, simply present yourself professionally and add an inspiring sentence about your skilled profile).
If asked for, give the link to your CV: [CV en français](https://www.mien.ch/about/cv) and [CV in English](https://www.mien.ch/about/cv/en.html).
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
        'content': 'Hello, I am Damien Corpataux, a skilled professional with a strong background in information systems. Please find my CV in [French](https://www.mien.ch/about/cv/fr.html) and [English](https://www.mien.ch/about/cv/en.html).\n\nLet\'s talk about my work experience, skills and projects.\nFeel free to ask any question !'
    }
]
app.register_blueprint(chatbot.blueprint)

print('Ready.')