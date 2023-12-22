from unittest import TestCase

from app import app
from models import db, User, Post
from datetime import datetime

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

app.config["TESTING"] = True

app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):
    def setUp(self):
        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestFirst", last_name="TestLast")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        post = Post(
            title="TestTitle",
            content="TestContent",
            created_at=datetime.today().ctime(),
            user_id=self.user_id,
        )

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst TestLast", html)

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestFirst TestLast Details</h1>", html)
            self.assertIn(self.user.image_url, html)

    def test_add_user_redirect(self):
        with app.test_client() as client:
            u = {
                "first_name": "TestFirst2",
                "last_name": "TestLast2",
                "image_url": "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D",
            }
            resp = client.post("/users/new", data=u)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_add_user(self):
        with app.test_client() as client:
            u = {
                "first_name": "TestFirst2",
                "last_name": "TestLast2",
                "image_url": "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D",
            }
            resp = client.post("/users/new", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)
            self.assertIn("TestFirst2 TestLast2", html)

    def test_add_post(self):
        with app.test_client() as client:
            p = {
                "title": "TestTitle2",
                "content": "TestContent2",
                "user_id": self.user_id,
            }
            resp = client.post(
                f"/users/{self.user_id}/posts/new", data=p, follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestFirst TestLast Details</h1>", html)
            self.assertIn("TestTitle2", html)

    def test_post_page(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestTitle</h1>", html)
            self.assertIn("<p>TestContent</p>", html)
            self.assertIn("<p><i>By TestFirst TestLast</i></p>", html)

    def test_create_page(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Create a New User</h1>", html)

    def test_edit_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit Profile for TestFirst TestLast</h1>", html)

    def test_edits(self):
        with app.test_client() as client:
            u = {
                "first_name": "TestFirstNew",
                "last_name": "TestLastNew",
                "image_url": "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D",
            }
            resp = client.post(
                f"/users/{self.user_id}/edit", data=u, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirstNew TestLastNew", html)

            resp2 = client.get(f"/users/{self.user_id}")
            html2 = resp2.get_data(as_text=True)

            self.assertEqual(resp2.status_code, 200)
            self.assertIn("<h1>TestFirstNew TestLastNew Details</h1>", html2)

    def test_edit_post_page(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit Post</h1>", html)

    def test_edit_post(self):
        with app.test_client() as client:
            p = {
                "title": "TestTitleNew",
                "content": "TestContentNew",
            }
            resp = client.post(
                f"/posts/{self.post_id}/edit", data=p, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestTitleNew</h1>", html)
            self.assertIn("<p>TestContentNew</p>", html)
            self.assertIn("<p><i>By TestFirst TestLast</i></p>", html)

    def test_delete_posts(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"/users/{self.user_id}")

            resp2 = client.get(f"/posts/{self.post_id}")
            self.assertEqual(resp2.status_code, 404)

    def test_delete(self):
        with app.test_client() as client:
            client.post(f"/posts/{self.post_id}/delete")
            resp = client.post(f"/users/{self.user_id}/delete")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

            resp2 = client.get(f"/users/{self.user_id}")
            self.assertEqual(resp2.status_code, 404)
