from datetime import datetime

from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __repr__(self) -> str:
        return f'Task: #{self.id}, email: {self.email}'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    status = db.Column(db.String(50), nullable=False)
    expect_hours = db.Column(db.Integer, nullable=True)
    expect_performed = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship(
        "Category", backref="Task", lazy="select", uselist=False
    )

    def __repr__(self) -> str:
        return f'Task: #{self.id}, description: {self.description}'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Task: #{self.id}, description: {self.description}'
