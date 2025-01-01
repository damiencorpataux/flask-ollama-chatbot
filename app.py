import flask
from flask_session import Session
import chatbot

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '6e3e77427ceab6bf6649d755'  # FIXME: Move to .env file
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

chatbot.initial_messages = initial_messages = [
    {
        'role': 'system',
        'content': 'Your mission is to answer questions about Damien Corpataux. Do not answer questions about any other topic. '
    }
]
app.register_blueprint(chatbot.blueprint)
