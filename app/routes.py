import re
from functools import wraps
from datetime import datetime
from flask import render_template, url_for, redirect, session, request, flash
from app import app, db
from app.models import Post, Tag


def login_required(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        if session.get("logged_in"):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()[::-1]  # reversed array of all posts.
    return render_template("index.html", title="rickblog home", posts=posts)


@app.route('/create/', methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        if request.form.get("title") and request.form.get("body"):
            title = request.form.get("title")
            body = request.form.get("body")
            slug = re.sub('[^\w]+', '-', title.lower()).strip('-')
            new_post = Post(title=title, body=body, slug=slug)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            flash("title and body required", "danger")
    return render_template("create.html")


@app.route('/login/', methods=["GET", "POST"])
def login():
    next_url = request.args.get("next") or request.form.get("next")
    if request.method == "POST" and request.form.get("password"):
        pw = request.form.get("password")
        if pw == app.config["ADMIN_PASSWORD"]:
            session["logged_in"] = True
            session.permanent = True
            return redirect(next_url or url_for('index'))
        else:
            flash("Incorrect password", "danger")
    return render_template("login.html", next_url=next_url)


@app.route('/logout/', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/<slug>/', methods=["GET"])
def detail(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template("detail.html", post=post)


@app.route('/edit/<slug>/', methods=["GET", "POST"])
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if request.method == "POST":
        post.title = request.form.get("title")
        post.body = request.form.get("body")
        post.slug = re.sub('[^\w]+', '-', post.title.lower()).strip('-')
        post.timestamp = datetime.utcnow()
        db.session.commit()
        return redirect(url_for("detail", slug=post.slug))
    return render_template("edit.html", post=post)
