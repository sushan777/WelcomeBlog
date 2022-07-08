from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .views import Create, List_View, Detail_View, Update, Delete

urlpatterns = [
path('',views.home, name = 'home'),
path('blogs/export',views.export, name = 'export'),
path('accounts/login/', views.login, name ='login'),
path('logout/', views.logout, name="logout"),
path('accounts/register/', views.register, name='register'),
path('accounts/profile/password/', views.change_password, name='change_password'),
path('blogs/create/', login_required(Create.as_view(),login_url="login"), name = 'create'),
path('blogs/listview/', login_required(List_View.as_view(),login_url="login"), name = 'listview'),
path('blogs/<pk>/', login_required(Detail_View.as_view(),login_url="login"), name = 'detailview'),
path('blogs/<pk>/update',login_required(Update.as_view(),login_url="login"), name = 'update'),
path('blogs/<pk>/delete',login_required(Delete.as_view(),login_url="login"), name = 'delete'),
path('blogs/search',views.search, name = 'search'),
path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
url(r'^accounts/profile/$', views.view_profile, name='view_profile'),
url(r'^accounts/profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),
url(r'^accounts/profile/edit/$', views.edit_profile, name='edit_profile'),
]