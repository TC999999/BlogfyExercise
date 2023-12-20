from unittest import TestCase

from app import app
from models import db, Users

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()


class BloglyModelTestCase(TestCase):
    def setUp(self):
        Users.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_update(self):
        user = Users(first_name="TestFirst", last_name="TestLast")
        user.update_user(
            "TestNewFirst",
            "TestNewLast",
            "https://upload.wikimedia.org/wikipedia/commons/d/d6/Nophoto.jpg",
        )

        self.assertEqual(user.first_name, "TestNewFirst")
        self.assertEqual(user.last_name, "TestNewLast")
