from django.conf import settings
from django.db import models
from django.urls import reverse

1
class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question_author')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_question', blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse("comm:detail", args=[self.pk])


class Answer(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answer_author')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_answer', blank=True)

    def __str__(self):
        return self.content[:10]


    class Meta:
        ordering = ['-created']
