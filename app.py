# Server Side
from dataclasses import field
from flask import Flask
# Create API / Resource : Design API Method / abort:Validator
# reqparse : Map Request / marshal_with : Call For POST
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)
# Model


class CityModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.String(100), nullable=False)
    weather = db.Column(db.String(100), nullable=False)
    people = db.Column(db.String(100), nullable=False)

    # Map db Model
    def __repr__(self):
        return f"City(name={name},temp={temp},weather={weather},people={people})"


db.create_all()

# Add Request Parser // POST METHOD
city_add_args = reqparse.RequestParser()
city_add_args.add_argument(
    "name", type=str, required=True, help="Please Request Name to String.")
city_add_args.add_argument(
    "temp", type=str, required=True, help="Please Request Temp to String.")
city_add_args.add_argument(
    "weather", type=str, required=True, help="Please Request Weather to String.")
city_add_args.add_argument(
    "people", type=str, required=True, help="Please Request People to String.")


# Update Request Parser // PATCH
city_update_args = reqparse.RequestParser()
city_update_args.add_argument(
    "name", type=str, help="Update Name.")
city_update_args.add_argument(
    "temp", type=str, help="Update Temp.")
city_update_args.add_argument(
    "weather", type=str,  help="Update Weather.")
city_update_args.add_argument(
    "people", type=str,  help="Update People.")

# Call Method fields
resource_field = {
    "id": fields.Integer,
    "name": fields.String,
    "temp": fields.String,
    "weather": fields.String,
    "people": fields.String,
}

# Design API Get Method


class WeatherCity(Resource):

    @marshal_with(resource_field)
    def get(self, city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404, msg="Not Found Data")
        return result

    @marshal_with(resource_field)
    def post(self, city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if result:
            abort(409, msg="city_ID already exist")
        args = city_add_args.parse_args()
        city = CityModel(
            id=city_id, name=args["name"], temp=args["temp"], weather=args["weather"], people=args["people"])
        db.session.add(city)
        db.session.commit()
        return city, 201

    @marshal_with(resource_field)
    def patch(self, city_id):
        args = city_update_args.parse_args()
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404, msg="Not Found Data for Update.")
        if args["name"]:
            result.name = args["name"]    # Update Name
        if args["temp"]:
            result.temp = args["temp"]    # Update Temp
        if args["weather"]:
            result.weather = args["weather"]    # Update Weather
        if args["people"]:
            result.people = args["people"]    # Update People
        
        db.session.commit()
        return result


# Call API & Rule
api.add_resource(WeatherCity, "/weather/<int:city_id>")

if __name__ == "__main__":
    app.run(debug=True)
