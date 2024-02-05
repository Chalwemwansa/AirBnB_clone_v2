#!/usr/bin/python3
"""python3 -c 'print(__import__("my_module").__doc__)'
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hbnb():
    """function that serves some html code if url is /
    """
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run()
