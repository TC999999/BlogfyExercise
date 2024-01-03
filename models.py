"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Creates Table for Users and updates user information on client side"""

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
        return f"<User id={p.id} first_name={p.first_name} last_name={p.last_name}>"

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
    """Creates Table for Posts based on users and updates post information on client side"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False, default=datetime.today().ctime())
    modified_last = db.Column(db.String, nullable=False, default="No Modifications")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    usr = db.relationship("User", backref="pst")

    pst_tgs = db.relationship("PostTag", backref="pst")

    tgs = db.relationship("Tag", secondary="post_tags", backref="pst")

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} user_id={p.user_id}>"

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


class Tag(db.Model):
    """Creates Table for Tags and updates tag information on client side"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    pst_tg = db.relationship("PostTag", backref="tg")

    def __repr__(self):
        t = self
        return f"<Tag id={t.id} name={t.name}>"

    def update_tag(self, n):
        self.name = n


class PostTag(db.Model):
    """Creates Table for relationship between posts and tags and updates relationship information on client side"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        pt = self
        return f"<PostTag post_id={pt.post_id} tag_id={pt.tag_id}>"
