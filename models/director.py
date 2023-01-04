from db import db

class DirectorModel(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    movies = db.relationship('MovieModel', back_populates='director', foreign_keys='MovieModel.director_id')


    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "movies": [movie.json() for movie in self.movies]   
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