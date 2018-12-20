import requests

from .secret import url1, url2
from .tools_classes import Book, Booklist


def api_login(form):
	"""
	API POST запрос авторизации
	:param form: форма с учетными данными email и password (forms.Form)
	:return:
	"""
	login_data = dict()
	login_data['email'] = form.cleaned_data['login']
	login_data['password'] = form.cleaned_data['password']
	response = requests.post(url1, json=login_data)
	return response


def make_booklist(resp_text):
	"""
	Формирование объекта Booklist с нужными полями
	:param resp_text: (dict)
	:return: (Booklist)
	"""
	booklist = Booklist()
	booklist.next_page = resp_text['meta']['next'] if resp_text['meta']['next'] else ''
	booklist.previous_page = resp_text['meta']['previous'] if resp_text['meta']['previous'] else ''
	for obj in resp_text['objects']:
		book = Book()
		book.name = obj['book']['name']
		book.authors_names = obj['book']['authors_names']
		book.add_cover_url(obj['book']['default_cover'])
		booklist.books_list.append(book)
	return booklist


def check_and_get_data(request):
	"""
	Проверка актуальности cookie сессии в браузере
	:param request:
	:return: (Booklist)
	"""
	browser_session_cookie = request.COOKIES.get('session')
	if not browser_session_cookie:
		return None
	else:
		return get_booklist(browser_session_cookie)


def get_booklist(browser_session_cookie):
	"""
	API GET запрос списка книг
	:param browser_session_cookie: сессионная cookie session браузера(str)
	:return: (Booklist)
	"""
	ses = requests.Session()
	ses.cookies.set('session', browser_session_cookie)
	ses.headers['Accept'] = 'application/json;version=5'
	response = ses.get(url2)
	if browser_session_cookie == response.cookies.get('session'):
		return None
	else:
		return make_booklist(response.json())
