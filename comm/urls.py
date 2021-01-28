from django.urls import path, re_path
from .views import *

app_name = 'comm'

urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:pk>/', detail, name='detail'),
    path('question/create/', question_create, name='question_create'),
    path('question/update/<int:pk>/', question_update, name='question_update'),
    path('question/delete/<int:pk>/', question_delete, name='question_delete'),
    path('answer/create/<int:pk>/', answer_create, name='answer_create'),
    path('answer/update/<int:answer_id>/', answer_update, name='answer_update'),
    path('answer/delete/<int:answer_id>/', answer_delete, name='answer_delete'),

    path('vote/question/<int:question_id>/', vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/', vote_answer, name='vote_answer'),
]

