"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(
        db.String,
        nullable=False,
        default="https://upload.wikimedia.org/wikipedia/commons/d/d6/Nophoto.jpg",
    )

    def __repr__(self):
        p = self
        return f"<User id={p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url}>"

    def update_user(self, f_n, l_n, i_u):
        self.first_name = f_n
        self.last_name = l_n
        if i_u == None:
            self.image_url = (
                "https://upload.wikimedia.org/wikipedia/commons/d/d6/Nophoto.jpg"
            )
        else:
            self.image_url = i_u


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False, default=datetime.today().ctime())
    modified_last = db.Column(db.String, nullable=False, default="No Modifications")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    usr = db.relationship("User", backref="pst")

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} title={p.title} created_at={p.created_at} modified_last={p.modified_last} user_id={p.user_id}>"

    def update_post(self, t, c, d):
        if t:
            self.title = t
        else:
            self.title = "NO TITLE"

        if c:
            self.content = c
        else:
            self.content = "NO CONTENT"

        self.modified_last = d
