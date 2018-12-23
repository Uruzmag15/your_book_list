import requests

from .secret import domain, auth_url, bookuserlist_url
from .tools_classes import Book, Booklist


def api_login(form):
	"""
	API POST запрос авторизации
	:param form: форма с учетными данными email и password (forms.Form)
	:return: (http response)
	"""
	login_data = dict()
	login_data['email'] = form.cleaned_data['login']
	login_data['password'] = form.cleaned_data['password']
	response = requests.post(auth_url, json=login_data)
	return response


def make_booklist(resp_dict):
	"""
	Формирование объекта Booklist с нужными полями
	:param resp_dict: словарь из JSON ответа API (dict)
	:return: экземпляр объекта(Booklist)
	"""
	try:
		booklist = Booklist()
		booklist.next_page = resp_dict['meta'].get('next') if resp_dict['meta'].get('next') else ''
		booklist.previous_page = resp_dict['meta'].get('previous') if resp_dict['meta'].get('previous') else ''
		for obj in resp_dict.get('objects'):
			book = Book()
			book.name = obj['book'].get('name')
			book.authors_names = obj['book'].get('authors_names')
			book.add_cover_url(obj['book'].get('default_cover'))
			booklist.books_list.append(book)
	except KeyError:
		return None
	return booklist


def get_booklist(browser_session_cookie, cursor):
	"""
	API GET запрос списка книг
	:param browser_session_cookie: сессионная cookie session браузера (str)
	:param cursor: кусок URL-а след./предыд. страницы из JSON ответа API (str)
	:return: словарь из JSON ответа API (dict)
	"""
	ses = requests.Session()
	ses.cookies.set('session', browser_session_cookie)
	ses.headers['Accept'] = 'application/json;version=5'
	url = '{}{}'.format(domain, cursor) if cursor else bookuserlist_url
	response = ses.get(url)
	return response.json()
