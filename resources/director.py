from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from models import DirectorModel
from schemas import DirectorSchema

blp = Blueprint("Directors", "directors", description="Operations on directors")


@blp.route("/director/<string:name>")
class Director(MethodView):
    @jwt_required()
    @blp.response(200, DirectorSchema)
    def get(self, name):
        director = DirectorModel.find_by_name(name)
        if director:
            return director
        abort(404, message="Director not found")

    @jwt_required(fresh=True)
    @blp.arguments(DirectorSchema)
    @blp.response(201, DirectorSchema)
    def post(self, director_data, name):
        if DirectorModel.find_by_name(name):
            abort(400, message=f"A director with name {name} already exists.")

        actor = DirectorModel(**director_data, name=name)

        try:
            actor.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the actor.")

        return actor

    @jwt_required()
    def delete(self, name):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            abort(401, message="Admin privilege required.")

        director = DirectorModel.find_by_name(name)
        if director:
            director.delete_from_db()
            return {"message": "Director deleted."}
        abort(404, message="Director not found.")


@blp.route("/director")
class DirectorList(MethodView):
    @jwt_required()
    @blp.response(200, DirectorSchema(many=True))
    def get(self):
        return DirectorModel.find_all()
