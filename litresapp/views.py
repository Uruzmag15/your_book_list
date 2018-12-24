from django.shortcuts import render
from django.http import HttpResponseRedirect

from .tools import api_login, get_booklist, make_booklist
from .forms import LoginForm


def book_list_view(request, **kwargs):
	browser_session_cookie = request.COOKIES.get('session')
	if not browser_session_cookie:
		return HttpResponseRedirect('/login/')

	api_response = get_booklist(browser_session_cookie, kwargs.get('cursor'))
	if not api_response:
		return HttpResponseRedirect('/login/')

	booklist = make_booklist(api_response)
	return render(request, 'litresapp/book_list.html', {'booklist': booklist})


def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			api_login_response = api_login(form)

			if api_login_response.status_code == 200:
				api_session_cookie = api_login_response.cookies.get('session')
				cks = {
					'key': 'session',
					'value': api_session_cookie,
					'path': '/',
					'domain': '127.0.0.1',
					'httponly': True
				}
				resp_redir = HttpResponseRedirect('/')
				resp_redir.set_cookie(**cks)
				return resp_redir

			elif api_login_response.status_code == 400:
				return render(request, 'litresapp/login.html', {'form': form, 'error_message': 'Неверный логин/пароль!'})

			else:
				form = LoginForm()
	else:
		form = LoginForm()
	return render(request, 'litresapp/login.html', {'form': form})


def logout_view(request):
	response = HttpResponseRedirect('/login/')
	response.delete_cookie('session')
	return response
