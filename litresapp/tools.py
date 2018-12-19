import requests
import json

from .secret import url1, url2


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


def check_and_get_data(request):
	"""
	Проверка актуальности cookie сессии в браузере
	:param request:
	:return: (dict)
	"""
	mb_session_cookie = request.COOKIES.get('session')
	if not mb_session_cookie:
		return None
	else:
		return get_booklist(mb_session_cookie)


def get_booklist(mb_session_cookie):
	"""
	API GET запрос списка книг
	:param mb_session_cookie: сессионная cookie session (str)
	:return: (dict)
	"""
	ses = requests.Session()
	ses.cookies.set('session', mb_session_cookie)
	response = ses.get(url2)

	if mb_session_cookie == response.cookies.get('session'):
		return None
	else:
		# return json.loads(response.text)
		return response.text
