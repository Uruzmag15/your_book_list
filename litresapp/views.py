from django.shortcuts import render
from django.http import HttpResponseRedirect

from .tools import check_and_get_data, api_login
from .forms import LoginForm


def book_list_view(request):
	booklist = check_and_get_data(request)
	if booklist:
		return render(request, 'litresapp/book_list.html', {'booklist': booklist})
	else:
		return HttpResponseRedirect('/login/')


def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			api_login_response = api_login(form)

			if api_login_response.status_code == 200:
				api_session_cookie = api_login_response.cookies.get('session')
				resp_redir = HttpResponseRedirect('/')
				resp_redir.set_cookie('session', value=api_session_cookie, httponly=True)
				return resp_redir

			elif api_login_response.status_code == 400:
				return render(request, 'litresapp/login.html', {'form': form, 'error_message': 'Incorrect login/password!'})

			else:
				form = LoginForm()
	else:
		form = LoginForm()
	return render(request, 'litresapp/login.html', {'form': form})


def logout_view(request):
	response = HttpResponseRedirect('/login/')
	response.delete_cookie('session')
	return response
