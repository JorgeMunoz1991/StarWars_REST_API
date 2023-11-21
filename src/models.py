from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {"id": self.id,
                "email": self.email,
                "is_active": self.is_active}


class People(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "name": self.name}


class UserFavoritesPlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    
    def __repr__(self):
        return '<UserFavoritesPlanets %r>' % self.id
    
    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "planet_id": self.planet_id}


class UserFavoritesPeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    def __repr__(self):
        return '<UserFavoritesPeople %r>' % self.id
    
    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "people_id": self.people_id}

