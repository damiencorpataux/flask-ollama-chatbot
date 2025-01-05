flask-ollama-chatbot
=
A simply basic Chatbot on Ollama and Flask.

Features:
- Minimal approach
- Customizable system prompt
- Initial messages translation
- Response streaming
- Runs locally using Ollama

Usage
-
Install Ollama (eg. for MacOS):
```sh
brew install ollama
ollama pull llama3.2
```

Install python requirements:
```sh
pip3 install -r requirements.txt
```

Run the example:
```sh
flask run
```

Open http://localhost:5000/


Demo
-
Click to play video (on YouTube):

[![Demonstration video](https://img.youtube.com/vi/HqmJNq8V2ss/0.jpg)](https://www.youtube.com/watch?v=HqmJNq8V2ss "Demonstration video")

The code is **4** files, **466** lines of code:
```sh
$ wc -l *.py chatbot/*.py chatbot/templates/*            
      44 app.py
     142 chatbot/__init__.py
     241 chatbot/templates/home.html
      39 chatbot/templates/html.html
     466 total
```