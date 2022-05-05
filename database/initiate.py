## seeds database with product information
## and fake user data

from database.user_db import connect_to_db, db, User
from app import app
from faker import Faker
# from HTMLParser import HTMLParser


N_USERS = 10


def create_users():
    """Creates fake users and loads them into the db"""

    # Instantiate a Faker object
    fake = Faker()
    fake.seed(435)

    # Create N user objects and add them to the db
    for i in range(N_USERS):

        user = User(name=fake.name(),
                    email=fake.email(),
                    password=fake.bs())

        db.session.add(user)

    db.session.commit()



##################### Run script #################################

if __name__ == "__main__":

    connect_to_db(app)

    # In case tables haven't been created, create them
    print("1")
    db.create_all()
    print("2")
    # H = HTMLParser()

    create_users()
