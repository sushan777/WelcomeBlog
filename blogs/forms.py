from django import forms
from .models import Category, Post, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

class Post(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	image = forms.ImageField()
	
	class Meta:
		model = Post

		fields = [
		'category',
		'title',
		'image',
		'summary',
		]

class RegistrationForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'form-control'}))
	password1 = forms.CharField(label ="Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label = "Confirm-Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	class Meta:
		model = User
		fields = (
        	'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
        
	def save(self, commit = True):
		user = super(RegistrationForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

		return user

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

class ProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = (
		 'description',
		 'city', 
		 'website', 
		 'phone',
		 'image') 