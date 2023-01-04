from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from models import MovieModel,ActorModel
from schemas import MovieSchema
from db import db

blp = Blueprint("movies", "movies", description="Operations on movies")


@blp.route("/movie/<string:name>")
class Movie(MethodView):
        
    @blp.response(200, MovieSchema)
    def get(cls, name):
        movie = MovieModel.find_by_name(name)
        if movie:
            return movie
        abort(404, message="Movie not found.")

    @blp.arguments(MovieSchema)
    @blp.response(201, MovieSchema)
    def post(self, movie_data, name):
        if MovieModel.find_by_name(name):
            abort(400, message=f"A movie with name '{name}' already exists.")

    # Unpack the movie_data dictionary and pass the key-value pairs as 
    # keyword arguments to the MovieModel constructor
        movie = MovieModel(**movie_data,name=name)
        actors = movie_data.pop("actors", [])  # extract actors from movie_data
        actor_objects = []
        for actor in actors:
            actor_obj = ActorModel.query.get(actor['id'])
            actor_objects.append(actor_obj)
        movie.actors = actor_objects

        try:
            db.session.add(movie)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the movie.")
        return movie

        
    @jwt_required()
    def delete(cls, name):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            abort(401, message="Admin privilege required.")
        movie = MovieModel.find_by_name(name)
        if movie:
            movie.delete_from_db()
            return {"message": "Movie deleted"}, 200
        abort(404, message="Movie not found.")

@blp.route("/movie")
class MovieList(MethodView):
    @blp.response(200, MovieSchema(many=True))
    def get(cls):
        return MovieModel.find_all()
