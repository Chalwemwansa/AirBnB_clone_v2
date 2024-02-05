#!/usr/bin/python3
"""python3 -c 'print(__import__("my_module").MyClass.__doc__)'
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states():
    """renders an html page that lists all the states in the database
    """
    from models import State
    state_list = storage.all(State).values()
    sorted_list = sorted(state_list, key=lambda obj: obj.name)
    return render_template('7-states_list.html', objs=sorted_list)


if __name__ == '__main__':
    app.run()
