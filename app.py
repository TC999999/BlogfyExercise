"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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
    """Redirects home to user page"""
    return redirect("/users")


@app.route("/users")
def user_list():
    """Renders page with a list of users"""
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def create_user():
    """Renders page to create new user"""
    return render_template("create.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Adds new user to db"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = str(image_url) if image_url else None

    if not first_name or not last_name:
        flash(
            "Please fill out both a first name AND a last name",
            "bg-warning mt-2 p-3 rounded",
        )
        return redirect("/users/new")
    else:
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Renders page for specified user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id)
    return render_template("details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Renders page to update user information"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def save_edit(user_id):
    """Updates user information to db"""
    edited_user = User.query.get(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = str(image_url) if image_url else None

    if not first_name or not last_name:
        flash(
            "Please make sure there's both a first name AND a last name",
            "bg-warning mt-2 p-3 rounded",
        )
        return redirect(f"/users/{user_id}/edit")
    else:
        edited_user.update_user(first_name, last_name, image_url)

        db.session.add(edited_user)
        db.session.commit()
        return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes user and any posts and relationships between posts and tags from db"""
    posts = Post.query.filter_by(user_id=user_id).all()
    for post in posts:
        PostTag.query.filter_by(post_id=post.id).delete()
    Post.query.filter_by(user_id=user_id).delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def post_page(user_id):
    """Renders page for a user to create a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Adds user's post to db"""
    title = request.form["title"]
    content = request.form["content"]
    if not title or not content:
        flash(
            "Please fill out both a title and some content",
            "bg-warning mt-2 p-3 rounded",
        )
        return redirect(f"/users/{user_id}/posts/new")
    else:
        created_at = datetime.today().ctime()
        tags = request.form.getlist("tag")
        new_tags = [PostTag(tag_id=i) for i in tags]

        new_post = Post(
            title=title,
            content=content,
            created_at=created_at,
            user_id=user_id,
            pst_tgs=new_tags,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Renders page of specified post"""
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes post and relationship between post and tags from db and returns to respective user page"""
    post_user_id = Post.query.get(post_id).user_id
    PostTag.query.filter_by(post_id=post_id).delete()
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/users/{post_user_id}")


@app.route("/posts/<int:post_id>/edit")
def edit_post_page(post_id):
    """Renders page to edit specified post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Updates post information to db"""
    edited_post = Post.query.get(post_id)
    title = request.form["title"]
    content = request.form["content"]
    if not title or not content:
        flash(
            "Please make sure this post has a title and some content",
            "bg-warning mt-2 p-3 rounded",
        )
        return redirect(f"/posts/{post_id}/edit")
    else:
        modified_last = datetime.today().ctime()
        tags = request.form.getlist("tag")
        edited_post.tgs.clear()
        for tag in tags:
            edited_post.tgs.append(Tag.query.get(tag))

        edited_post.update_post(title, content, modified_last)

        db.session.add(edited_post)
        db.session.commit()
        return redirect(f"/posts/{post_id}")


@app.route("/tags")
def tag_list():
    """Renders page with a list of tags"""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route("/tags/new")
def create_tag():
    """Renders page to add a tag"""
    return render_template("add_tag.html")


@app.route("/tags/new", methods=["POST"])
def render_tag():
    """Adds new tag to db"""
    name = request.form["name"]
    if not name:
        flash(
            "Please add a tag name",
            "bg-warning mt-2 p-3 rounded",
        )
        return redirect("/tags/new")
    else:
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def posts_in_tags(tag_id):
    """Renders page that shows list of posts that have specified tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_details.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_page(tag_id):
    """Renders page to edit specified tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Updates tag information to db"""
    edited_tag = Tag.query.get(tag_id)
    name = request.form["name"]
    if not name:
        flash(
            "Please make sure this tag has a name",
            "bg-warning mt-2 p-3 rounded",
        )
        return redirect(f"/tags/{tag_id}/edit")
    else:
        edited_tag.update_tag(name)

        db.session.add(edited_tag)
        db.session.commit()
        return redirect(f"/tags/{tag_id}")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Deletes tag and relationship to post from db"""
    PostTag.query.filter_by(tag_id=tag_id).delete()
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect("/tags")
