from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from sqlalchemy.inspection import inspect

# Get an Inspector object for your models
inspector = inspect(db.engine)

# Get a list of all of the relationships in your models
relationships = inspector.get_relationships()

# Iterate over the list of relationships and print the details
for relationship in relationships:
    print(f"{relationship.parent_entity}: {relationship.parent_property} -> {relationship.child_entity}: {relationship.child_property}")