import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, UserFavoritesPlanets, UserFavoritesPeople


app = Flask(__name__)
app.url_map.strict_slashes = False


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    results = [user.serialize() for user in users]
    response_body = {"message": "ok",
                     "total_records": len(results),
                     "results": results}
    return jsonify(response_body), 200


@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.get_json()
    user = User(email = request_body['email'],
                password = request_body['password'],
                is_active = request_body['is_active'])
    db.session.add(user)
    db.session.commit()
    return jsonify(request_body), 200


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    results = [character.serialize() for character in people]
    response_body = {"message": "ok",
                     "total_records": len(results),
                     "results": results}
    return jsonify(response_body), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    people = db.get_or_404(People, people_id)
    result = people.serialize()
    response_body = {"message": "ok",
                     "result": result}
    return jsonify(response_body), 200


@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    results = [planet.serialize() for planet in planets]
    response_body = {"message": "ok",
                     "total_records": len(results),
                     "results": results}
    return jsonify(response_body), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = db.get_or_404(Planet, planet_id)
    result = planet.serialize()
    response_body = {"message": "ok",
                     "result": result}
    return jsonify(response_body), 200


@app.route('/user/favorites-planets/<int:user_id>', methods=['GET'])
def get_favorites_planets(user_id):
    favorites = UserFavoritesPlanets.query.filter(UserFavoritesPlanets.user_id == user_id).all()
    results = [favorite.serialize() for favorite in favorites]
    response_body = {"message": "ok",
                     "total_records": len(results),
                     "results": results}
    return jsonify(response_body), 200


@app.route('/favorite/planet', methods=['POST'])
def add_favorites_planets():
    request_body = request.get_json()
    favorite = UserFavoritesPlanets(user_id = request_body['user_id'],
                                    planet_id = request_body['planet_id'])
    db.session.add(favorite)
    db.session.commit()
    return jsonify(request_body), 200


@app.route("/user/favorites-planets/<int:favorite_id>", methods = ["DELETE"])
def delete_favorite_planet(favorite_id):
    favorites = UserFavoritesPlanets.query.get(favorite_id)
    if favorites is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorites)
    db.session.commit()
    return jsonify("Ok"), 200


@app.route('/user/favorites-people/<int:user_id>', methods=['GET'])
def get_favorites_people(user_id):
    favorites = UserFavoritesPeople.query.filter(UserFavoritesPeople.user_id == user_id).all()
    results = [favorite.serialize() for favorite in favorites]
    response_body = {"message": "ok",
                     "total_records": len(results),
                     "results": results}
    return jsonify(response_body), 200


@app.route('/favorite/people', methods=['POST'])
def add_favorites_people():
    request_body = request.get_json()
    favorite = UserFavoritesPeople(user_id = request_body['user_id'],
                                    people_id = request_body['people_id'])
    db.session.add(favorite)
    db.session.commit()
    return jsonify(request_body), 200


@app.route("/user/favorites-people/<int:favorite_id>", methods = ["DELETE"])
def delete_favorite_people(favorite_id):
    favorites = UserFavoritesPeople.query.get(favorite_id)
    if favorites is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorites)
    db.session.commit()
    return jsonify("Ok"), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
