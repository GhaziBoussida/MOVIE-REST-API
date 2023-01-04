from db import db

class ActorModel(db.Model):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

    
    movies = db.relationship('MovieModel', back_populates='actors', secondary='movie_actors')


    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "movies": [movie.json() for movie in self.movies.all()],
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
