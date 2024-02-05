#!/usr/bin/python3
"""python3 -c 'print(__import__("my_module").MyClass.__doc__)'
"""
from flask import Flask, render_template
from models import storage, State
app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception=None):
    """ calls the close method on storage with every request
    """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities():
    """renders an html page that lists the states and the cities in them
    """
    state_list = storage.all(State).values()
    sorted_list = sorted(state_list, key=lambda obj: obj.name)
    for state in sorted_list:
        state.cities = sorted(state.cities, key=lambda city: city.name)
    return render_template('8-cities_by_states.html', objs=sorted_list)


if __name__ == '__main__':
    app.run()
