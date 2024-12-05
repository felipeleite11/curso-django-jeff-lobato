from django.http import HttpResponseRedirect
from django.contrib.auth import logout as authLogout, login, authenticate
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def logout(request):
	authLogout(request)

	return HttpResponseRedirect(reverse('login'))

def register(request):
	if request.method != 'POST':
		form = UserCreationForm()
	else:
		form = UserCreationForm(data=request.POST)

		if form.is_valid():
			new_user = form.save()

			authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])

			login(request, authenticated_user)

			return HttpResponseRedirect(reverse('index'))
		
	context = {'form': form}

	return render(request, 'users/register.html', context)