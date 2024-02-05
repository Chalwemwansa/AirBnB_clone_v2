#!/usr/bin/python3
"""python3 -c 'print(__import__("my_module").__doc__)'
"""
from flask import Flask, render_template
from markupsafe import escape
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def welcome():
    """function that serves some html code if url is /
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """displays hbnb when /hbnb path is used
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def C(text):
    """displays a custom string on to the browser
    """
    mod_string = text.replace('_', ' ')
    return f"C {escape(mod_string)}"


@app.route('/python', defaults={'text', "is cool"},
           strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """displays python followed by a custom string where
       the default is 'is cool'
    """
    return f"Python {escape(text.replace('_', ' '))}"


@app.route('/number/<int:n>', strict_slashes=False)
def is_it_int(n):
    """checks if n is an integer or not
    """
    return f"{escape(n)} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def template(n):
    """checks if n is an int and serves an html page if its the case
    """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def old_or_even(n):
    """checks is n is old or even and does something based on that
    """
    if n % 2 == 0:
        value = f"{n} is even"
    else:
        value = f"{n} is odd"

    return render_template('6-number_odd_or_even.html',
                           value=value)


if __name__ == '__main__':
    app.run()
