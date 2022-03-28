from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    usertype = db.Column(db.Enum("developer", "designer", "manager", name="UserTypes"), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "usertype": self.usertype,
            # do not serialize the password, its a security breach
        }

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todos = db.Column(db.String(120), unique=False, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    todo_type = db.Column(db.Enum("bug/issue", "feature", "improvements", name="TodoTypes"), unique=False, nullable=False)
    stage = db.Column(db.Enum("notdone", "inprogress", "done", name="Stage"), unique=False, nullable=False)
    acceptance = db.Column(db.Enum("approved", "rejected", "furtherreview", name="Acceptance"), unique=False, nullable=False)
    due_date = db.Column(db.Date(), nullable=True)
    details = db.Column(db.String(250), unique=False, nullable=True)
    created_at = db.Column(db.DateTime(timezone=False), nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=False), nullable=True, onupdate=datetime.utcnow)
    user = db.relationship(User)


    def serialize(self):
        return {
            "id": self.id,
            "todos": self.todos,
            "todo_type": self.todo_type,
            "stage": self.stage,
            "acceptance": self.acceptance,
            "due_date": self.due_date,
            "details": self.details,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }