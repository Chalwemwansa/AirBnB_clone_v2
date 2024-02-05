#!/usr/bin/python3
"""python3 -c 'print(__import__("my_module").MyClass.__doc__)'
"""
from flask import Flask, render_template
from models import storage, State, Amenity
app = Flask(__name__)
state_list = storage.all(State).values()
sorted_list = sorted(state_list, key=lambda obj: obj.name)
for state in sorted_list:
    state.cities = sorted(state.cities, key=lambda city: city.name)


@app.teardown_appcontext
def close_session(exception=None):
    """ calls the close method on storage with every request
    """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_static():
    """deploys the airbnb static pages
    """
    amenity_list = storage.all(Amenity).values()
    sorted_amenity = sorted(amenity_list, key=lambda obj: obj.name)

    return render_template('10-hbnb_filters.html', amenity_list=sorted_amenity, objs=sorted_list)


if __name__ == '__main__':
    app.run()
