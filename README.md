flask-ollama-chatbot
=
A simply basic Ollama chatbot on Flask. LLM is running locally.


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

[![Demonstration video](https://img.youtube.com/vi/zbxCjDpgnRE/0.jpg)](https://www.youtube.com/watch?v=zbxCjDpgnRE "Demonstration video")

The code is **4** files, **322** lines of code:
```sh
$ wc -l *.py chatbot/*.py chatbot/templates/*
      42 app.py
      61 chatbot/__init__.py
     185 chatbot/templates/home.html
      34 chatbot/templates/html.html
     322 total
```