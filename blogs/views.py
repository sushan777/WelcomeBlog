import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyasn1.type.univ import Null
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post as Posts
from .forms import Post
from .forms import (
    RegistrationForm, EditProfileForm, EditProfileForm, ProfileForm)
from django.urls import reverse
from django.contrib import auth,messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

def export(request):
	scope = ["htpps://googleapis.com/auth/spreadsheets.edit"]
	gc = gspread.service_account(filename = "credentials.json")
	sheet = gc.open("User").sheet1
	datas = Posts.objects.all()
	sheet.insert_row(['User', 'Name','Category', 'Title','Summary'])
	for data in datas:
		sheet.insert_row([data.user.username, data.user.first_name + " " + data.user.last_name, data.category.category_type, data.title, data.summary_stripped],2)
	return redirect('home')
	
def home(request):
	post = {}
	items = Posts.objects.all()
	p = Paginator(items, 4)
	page_num = request.GET.get('page', 1)
	try:
		page = p.page(page_num)
	except EmptyPage:
		page = p.page(1)
	post = {'posts' : page}

	return render(request, 'blogs/index.html',post )

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully created")
			return redirect('login')
		
	else:
		form = RegistrationForm()
	args = {'form': form}

	return render(request, 'accounts/reg_form.html', args)


def login(request):
	if request.method == 'POST':

		user = auth.authenticate(request, username = request.POST['username'],password = request.POST['password'])
		if user is not None:
			auth.login(request,user)
			messages.add_message(request, messages.SUCCESS, 'Login Successful')
			return redirect('listview')

		else:
			messages.add_message(request, messages.ERROR, 'Username and Passwords DO NOT MAtch')
			return redirect('login')
	else:
 		return render(request, 'accounts/login.html')

def logout(request):
	auth.logout(request)
	messages.add_message(request, messages.SUCCESS, 'Successfully logged_out')
	return redirect('login')

@login_required(login_url="login")
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
        data = Posts.objects.filter(user=user)
    args = {'user': user, 'posts':data}
    return render(request, 'accounts/profile.html', args)

@login_required(login_url="login")
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect(reverse('view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'accounts/edit_profile.html', args)

@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.add_message(request, messages.SUCCESS, 'Password Changed Successfully')
            return redirect(reverse('view_profile'))
        else:
        	messages.add_message(request, messages.SUCCESS, 'Use authorized keywords')
        	return redirect(reverse('change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

class Create(SuccessMessageMixin, CreateView):
	model = Posts
	form_class = Post
	template_name = 'blogs/create_form.html'
	
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
	success_url = '/blogs/listview'
	success_message = "Blog titled %(title)s was sucessfully created"

class List_View(ListView):
	model = Posts
	template_name = 'blogs/blogs_list.html'
	paginate_by = 3
	def get_queryset(self):
		return Posts.objects.filter(user=self.request.user)

class Detail_View(DetailView):
	model = Posts
	template_name = 'blogs/blogs_detail.html'

class Update(SuccessMessageMixin,UpdateView):
	model = Posts
	form_class = Post
	template_name = 'blogs/edit_form.html'
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
	
	success_url = '/blogs/listview'
	success_message = "Blog titled %(title)s was sucessfully updated"

class Delete(DeleteView):
	model = Posts
	success_url = '/blogs/listview'
	success_message = "Blog titled %(title)s was sucessfully deleted"

	def delete(self, request, *args, **kwargs):
		obj = self.get_object()
		messages.success(self.request, self.success_message % obj.__dict__)
		return super(Delete, self).delete(request, *args, **kwargs)



def search(request):
	if request.method == 'POST':
		searched = request.POST['searched']
		blogs = Posts.objects.filter(title__icontains = searched)
		return render(request, 'blogs/search.html', {'searched':searched, 'blogs':blogs})
	else:
		return render(request, 'blogs/search.html', {})