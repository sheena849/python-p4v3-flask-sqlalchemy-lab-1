
# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

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
def earthquakes(id):
    earthquake =Earthquake.query.filter_by(id=id).first()
    if earthquake:
        return jsonify ({
        "id": earthquake.id,
        "magnitude":earthquake.magnitude,
        "location": earthquake.location,
        "year":earthquake.year
        })


    else:
      return make_response(
          jsonify({f"message": f"Earthquake {id} not found."}), 
          404
      )

@app.route('/earthquakes/magnitude/<float:magnitude>')
def quakes(magnitude):
    earthquakes= Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    earthquake_data=[
        {
            "id": earthquake.id,
            "magnitude":earthquake.magnitude,
            "location":earthquake.location,
            "year":earthquake.year
        }
        for earthquake in earthquakes
    ]
    return jsonify({
        "count":len(earthquakes),
        "quakes": earthquake_data
    })
    





if __name__ == '__main__':
    app.run(port=5555, debug=True)
