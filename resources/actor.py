from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from models import ActorModel,MovieModel
from schemas import ActorSchema,ActorMovieSchema
from db import db
blp = Blueprint("Actors", "actors", description="Operations on actors")


@blp.route("/actor/<string:name>")
class Actor(MethodView):
    @jwt_required()
    @blp.response(200, ActorSchema)
    def get(self, name):
        actor = ActorModel.find_by_name(name)
        if actor:
            return actor
        abort(404, message="Actor not found")

    @jwt_required(fresh=True)
    @blp.arguments(ActorSchema)
    @blp.response(201, ActorSchema)
    def post(self, actor_data, name):
        if ActorModel.find_by_name(name):
            abort(400, message=f"An actor with name {name} already exists.")
      
        movies = actor_data.pop("movies", [])  # extract movies from actor_data
        actor = ActorModel(**actor_data, name=name)

        try:
            db.session.add(actor)
            for movie in movies:
                movie_obj = MovieModel.query.get(movie['id'])
                actor.movies.append(movie_obj)
            db.session.commit()
            #actor.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the actor.")

        return actor

    @jwt_required()
    def delete(self, name):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            abort(401, message="Admin privilege required.")

        actor = ActorModel.find_by_name(name)
        if actor:
            actor.delete_from_db()
            return {"message": "Actor deleted."}
        abort(404, message="Actor not found.")


@blp.route("/actor")
class ActorList(MethodView):
    @blp.response(200, ActorSchema(many=True))
    def get(self):
        return ActorModel.find_all()

@blp.route("/movie/<int:movie_id>/actor/<int:actor_id>")
class LinkActorssToMovie(MethodView):
    @jwt_required()
    @blp.response(201, ActorSchema)
    def post(self, movie_id, actor_id):
        movie = MovieModel.query.get_or_404(movie_id)
        actor = ActorModel.query.get_or_404(actor_id)

        movie.actors.append(actor)

        try:
            db.session.add(movie)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the actor.")

        return actor
    @jwt_required()
    @blp.response(200, ActorMovieSchema)
    def delete(self, movie_id, actor_id):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            abort(401, message="Admin privilege required.")    
        movie = MovieModel.query.get_or_404(movie_id)
        actor = ActorModel.query.get_or_404(actor_id)
        try:
            movie.actors.remove(actor)
        except ValueError:
            abort(404, message="Actor not found in movie.")
        try:
            db.session.add(movie)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the actor.")

        return {"message": "Actor removed from Movie", "movie": movie, "actor": actor}
