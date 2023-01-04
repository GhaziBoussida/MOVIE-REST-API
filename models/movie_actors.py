from db import db

class MovieActors(db.Model):
    __tablename__= "movie_actors"
    id = db.Column(db.Integer,primary_key=True)
    movie_id=db.Column(db.Integer, db.ForeignKey('movies.id'))
    actor_id=db.Column( db.Integer, db.ForeignKey('actors.id'))
    