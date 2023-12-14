from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()


class User(db.Model):
    """User object"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        """Display when printing a User object"""

        return "<User: {} email: {}>".format(self.user_id, self.email)

    @classmethod
    def register_user(cls, name, email, password):
        """Register a new user"""

        user = cls(name=name,
                   email=email,
                   password=password)

        # Add user to the session
        db.session.add(user)

        # Commit transaction to db
        db.session.commit()


def connect_to_db(app,db_uri ):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    # Work with database directly if run interactively

    from app import app
    connect_to_db(app)
