from .secret import media_url


class Book:
	def __init__(self):
		self.name = None
		self.authors_names = None
		self.default_cover = None

	def add_cover_url(self, url):
		self.default_cover = '{}{}'.format(media_url, url)


class Booklist:
	def __init__(self):
		self.next_page = None
		self.previous_page = None
		self.books_list = []
