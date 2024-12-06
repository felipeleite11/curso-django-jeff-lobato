from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(
		required=False,
	)
	password = forms.CharField(
		widget=forms.PasswordInput,
		required=False,
	)

	class Meta:
		model = User
		fields = ['username', 'password']
		labels = {'username': 'Login', 'password': 'Senha'}
		help_texts = {'username': ''}

		# Apply placeholder
		# widgets = {
        #     'username': forms.TextInput(attrs={'placeholder': 'Seu login'}),
        # }
