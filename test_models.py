from unittest import TestCase

from app import app
from models import db, User, Post
from datetime import datetime

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()


class BloglyModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        Post.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_update_user(self):
        user = User(first_name="TestFirst", last_name="TestLast")
        user.update_user(
            "TestNewFirst",
            "TestNewLast",
            "https://upload.wikimedia.org/wikipedia/commons/d/d6/Nophoto.jpg",
        )

        self.assertEqual(user.first_name, "TestNewFirst")
        self.assertEqual(user.last_name, "TestNewLast")

    def test_update_post(self):
        post = Post(
            title="TestTitle",
            content="TestContent",
            created_at=datetime.today().ctime(),
            user_id=1,
        )
        post.update_post("TestNewTitle", "TestNewContent", datetime.today().ctime())
        self.assertEqual(post.title, "TestNewTitle")
        self.assertEqual(post.content, "TestNewContent")
