from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {"id": self.id,
                "email": self.email,
                "is_active": self.is_active}


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "hair_color": self.hair_color}


class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "name": self.name}

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    people_id= db.Column(db.Integer, db.ForeignKey('people.id'),nullable=True)
    planets_id= db.Column(db.Integer, db.ForeignKey('planets.id'),nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    people = db.relationship('People', backref='favorite', lazy=True, cascade='all, delete-orphan')
    planets = db.relationship('Planet', backref='favorite', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        people_query= People.query.filter_by(id= self.people_id).first()

        if people_query is None:
          people_resultado=  None
        else:
          people_resultado= people_query.serialize()['name']

        planet_query= Planet.query.filter_by(id= self.planets_id).first()

        if planet_query is None:
          planet_resultado=  None
        else:
          planet_resultado= planet_query.serialize()['name']
        

        return {
            "id": self.id,
            "people": people_resultado,
            "planets": planet_resultado,
            "user_id": self.user_id
        }
