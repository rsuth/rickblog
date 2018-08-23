from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    posts = [{'title': "first blog post", 'body': "this is the first blog post in a series of blog posts. it is a test."}, {
        'title': "second blog post", 'body': "this is the second blog post in the series, it is also a test."}]
    return render_template("index.html", title="rickblog home", posts=posts)
