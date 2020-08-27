import datetime

from webapp import db

tags = db.Table('post_tag', db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
				db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)
	text = db.Column(db.Text, nullable=False)
	tags = db.relationship('Tag', secondary=tags, backref='posts', lazy='dynamic')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	created_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

	def __repr__(self):
		return f"<Post {self.title}>"


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False, unique=True)

	def __init__(self, title=""):
		self.title = title

	def __repr__(self):
		return f"<Tag {self.title}>"
