# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import Earthquake

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_by_id(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        response = {
            "id": earthquake.id,
            "magnitude": earthquake.magnitude,
            "location": earthquake.location,
            "year" : earthquake.year
        }
        return make_response(jsonify(response), 200)
    else:
        response = {"message": f"Earthquake {id} not found."}
        return make_response(jsonify(response), 404)
    

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    quakes_list = [
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        } for quake in earthquakes
    ]

    response = {
        "count": len(quakes_list),
        "quakes": quakes_list
    }

    return make_response(jsonify(response), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
