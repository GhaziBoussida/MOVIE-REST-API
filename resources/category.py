from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from models import CategoryModel
from schemas import CategorySchema

blp = Blueprint("Categories", "categories", description="Operations on categories")


@blp.route("/category/<string:name>")
class Category(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema)
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category
        abort(404, message="Category not found")

    @jwt_required(fresh=True)
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data, name):
        if CategoryModel.find_by_name(name):
            abort(400, message=f"A category with name {name} already exists.")

        actor = CategoryModel(**category_data, name=name)

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

        category = CategoryModel.find_by_name(name)
        if category:
            category.delete_from_db()
            return {"message": "Category deleted."}
        abort(404, message="Category not found.")


@blp.route("/category")
class CategoryList(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.find_all()
