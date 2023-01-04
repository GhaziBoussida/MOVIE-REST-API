from db import db


class MovieModel(db.Model):
    __tablename__="movies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    release_date = db.Column(db.String(30))
    description = db.Column(db.String(500))

    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    director = db.relationship('DirectorModel', back_populates='movies')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('CategoryModel', back_populates='movies')

    actors = db.relationship('ActorModel', back_populates='movies', secondary='movie_actors')

    
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "release_date": self.release_date,
            "description": self.description,
            "actors": [actor.json() for actor in self.actors.all()],
            "director": self.director.json() if self.director is not None else None,
            "category": self.category.json() if self.category is not None else None
        }
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()