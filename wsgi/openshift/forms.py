from django.contrib.auth.models import User
from django.forms import forms
from schedules.models import Faculty


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ('website', 'picture')