from django.urls import path, re_path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
app_name = 'accounts'

urlpatterns = [
    path('account/', include('allauth.urls')),
    path('login/', LoginView.as_view(template_name="accounts/login_form.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', password_change, name='password_change'),
    path('signup/', signup, name='signup'),
    path('edit/', profile_edit, name='profile_edit'),

    re_path(r'^(?P<username>[\w.@+-]+)/follow/$', user_follow, name='user_follow'),
    re_path(r'^(?P<username>[\w.@+-]+)/unfollow/$', user_unfollow, name='user_unfollow'),
]