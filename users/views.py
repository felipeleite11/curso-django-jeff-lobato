from django.http import HttpResponseRedirect
from django.contrib.auth import logout as authLogout, authenticate
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as authLogin
from .forms import LoginForm

def login(request):
	error = None

	if request.method != 'POST':
		form = LoginForm()

	else:
		form = LoginForm(data=request.POST)

		if form.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')

			if username == '' or password == '':
				error = 'Usuário e senha são obrigatórios.'

			else:
				user = authenticate(username=username, password=password)

				if user:
					authLogin(request, user)

					return HttpResponseRedirect(reverse('auth_index'))
				
				else:
					error = 'Usuário e/ou senha incorreta.'
			
	context = {'form': form, 'error': error}

	return render(request, 'users/login.html', context)

def logout(request):
	authLogout(request)

	return HttpResponseRedirect(reverse('login'))

def register(request):
	if request.method != 'POST':
		form = UserCreationForm()

	else:
		form = UserCreationForm(data=request.POST)

		print(form.data)

		if form.is_valid():
			new_user = form.save()

			authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])

			authLogin(request, authenticated_user)

			return HttpResponseRedirect(reverse('index'))
		
	context = {'form': form}

	return render(request, 'users/register.html', context)