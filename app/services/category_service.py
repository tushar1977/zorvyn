from app.extensions import db
from app.models.category import Category
from app.utils.validator import validate_category_type


def get_categories():
    return Category.query


def create_category(data):
    name = data.get("name")
    if not name:
        raise ValueError("name is required")

    category_type = validate_category_type(data.get("type"))

    category = Category(name=name, type=category_type)

    db.session.add(category)
    db.session.commit()

    return category


def seed_categories():
    categories = [
        {"name": "Food", "type": "expense"},
        {"name": "Salary", "type": "income"},
    ]

    for c in categories:
        existing = Category.query.filter_by(name=c["name"]).first()
        if not existing:
            category = Category(name=c["name"], type=validate_category_type(c["type"]))
            db.session.add(category)

    db.session.commit()
    return categories
