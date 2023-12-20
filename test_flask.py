from unittest import TestCase

from app import app
from models import db, Users

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

app.config["TESTING"] = True

app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):
    def setUp(self):
        Users.query.delete()

        user = Users(first_name="TestFirst", last_name="TestLast")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

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

    def test_delete(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

            resp2 = client.get(f"/users/{self.user_id}")
            self.assertEqual(resp2.status_code, 404)
