"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "bloglyylgolbkltpzyxm"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def to_users():
    return redirect("/users")


@app.route("/users")
def user_list():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def create_user():
    return render_template("create.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = str(image_url) if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id)
    return render_template("details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def save_edit(user_id):
    edited_user = User.query.get(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = str(image_url) if image_url else None

    edited_user.update_user(first_name, last_name, image_url)

    db.session.add(edited_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def post_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("post.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    title = request.form["title"]
    if title:
        title = str(title)
    else:
        title = "NO TITLE"

    content = request.form["content"]
    if content:
        content = str(content)
    else:
        content = "NO CONTENT"

    created_at = datetime.today().ctime()

    new_post = Post(
        title=title,
        content=content,
        created_at=created_at,
        user_id=user_id,
    )
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post_user_id = Post.query.get(post_id).user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/users/{post_user_id}")


@app.route("/posts/<int:post_id>/edit")
def edit_post_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    edited_post = Post.query.get(post_id)
    title = request.form["title"]
    content = request.form["content"]
    modified_last = datetime.today().ctime()

    edited_post.update_post(title, content, modified_last)

    db.session.add(edited_post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")
