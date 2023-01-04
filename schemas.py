from marshmallow import Schema, fields

class PlainActorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(nullable=False)

class PlainMovieSchema(Schema):
    id = fields.Int()
    name = fields.Str(nullable=False)
    release_date = fields.Str()
    description = fields.Str()

class MovieWithoutDirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str(nullable=False)
    release_date = fields.Str()
    description = fields.Str()
    actors = fields.List(fields.Nested(PlainActorSchema), many=True,dump_only=True) 
class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(nullable=False)
    movies = fields.List(fields.Nested(MovieWithoutDirectorSchema))

class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(nullable=False)
    movies = fields.List(fields.Nested(MovieWithoutDirectorSchema))
class ActorSchema(PlainActorSchema):
    movies = fields.List(fields.Nested(PlainMovieSchema))
class MovieSchema(PlainMovieSchema):
    director_id = fields.Int()
    director= fields.Nested(DirectorSchema)
    actors= fields.List(fields.Nested(PlainActorSchema), many=True)
    category_id = fields.Int()
    category= fields.Nested(CategorySchema)

class ActorMovieSchema(Schema):
    movie = fields.Nested(MovieSchema)
    actor = fields.Nested(ActorSchema)
class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(load_only=True)

