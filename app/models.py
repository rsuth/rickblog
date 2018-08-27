from datetime import datetime
from app import db

# this is a helper table, which defines the many to many relationship between
# posts and tags.
tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey(
                    'tag.id'), primary_key=True),
                db.Column('post_id', db.Integer, db.ForeignKey(
                    'post.id'), primary_key=True)
                )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    slug = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    tags = db.relationship('Tag', secondary=tags,
                           lazy='subquery',
                           backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post id {}: {}>'.format(self.id, self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)
