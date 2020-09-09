import random

from faker import Faker

from webapp import db, create_app
from webapp.auth.models import User, Role
from webapp.blog.models import Post, Tag


TAGS = ['Politic', 'USA', 'USSR', 'Media', 'IT']
app = create_app()


class FakeData:
	def __init__(self, faker):
		self.faker = faker
		self.users = []
		self.tags = []

	def _insert_to_db(self, model):
		try:
			db.session.add(model)
			db.session.commit()
		except Exception:
			db.session.rollback()
			raise

	def create_users(self, n, clear=False):
		if clear:
			User.query.delete()
			db.session.commit()

		for _ in range(n):
			user = User()
			user.username = self.faker.first_name()
			user.password = self.faker.word()
			self._insert_to_db(user)
			self.users.append(user)

	def _create_tag(self, clear=True):
		if clear:
			Tag.query.delete()
			db.session.commit()

		for title in TAGS:
			tag = Tag(title=title)
			self._insert_to_db(tag)
			self.tags.append(tag)

	def create_post(self, n, clear=False):
		if clear:
			Post.query.delete()
			db.session.commit()
		self._create_tag()
		for _ in range(n):
			post = Post()
			post.title = self.faker.sentence(nb_words=6)
			post.text = self.faker.text(max_nb_chars=2500)
			post.user_id = random.choice([user.id for user in self.users])
			post.created_at = self.faker.date_this_century()
			post.tags = [random.choice(self.tags) for _ in range(random.randint(1, 3))]
			self._insert_to_db(post)


if __name__ == "__main__":
	with app.app_context():
		fake_data = FakeData(Faker())
		fake_data.create_users(20, clear=True)
		fake_data.create_post(100, clear=True)
