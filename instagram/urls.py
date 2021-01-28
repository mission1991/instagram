from django.urls import path, re_path
from .views import *

app_name = 'instagram'

urlpatterns = [
    path('', index, name='index'),
    path('post/new/', post_new, name='post_new'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/like/', post_like, name='post_like'),
    path('post/<int:pk>/unlike/', post_unlike, name='post_unlike'),
    path('post/<int:post_pk>/comment/new/', comment_new, name='comment_new'),
    path('post/update/<int:pk>/', post_update, name='post_update'),
    path('post/delete/<int:pk>/', post_delete, name='post_delete'),
    re_path(r'^(?P<username>[\w.@+-]+)/$', user_page, name='user_page'),
    path('comment/delete/<int:pk>/', comment_delete, name='comment_delete'),


    re_path(r'^(?P<username>[\w.@+-]+)/follower_list/$', follower_list, name='follower_list'),
    re_path(r'^(?P<username>[\w.@+-]+)/following_list/$', following_list, name='following_list')
]
