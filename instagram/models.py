import re
from django.conf import settings
from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# user
#  -> Post.objects.filter(author=user)
#  -> user.post_set.all()

class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post_set', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/")
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank=True)
    tag_post = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_post_set')

    image_thumbnail = ImageSpecField(source='photo', processors=[ResizeToFill(512, 512)])

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.tag_post)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("instagram:post_detail", args=[self.pk])

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()
        # 유저가 좋아한다면 True / False 값으로 반환

    class Meta:
        ordering = ['-id']


class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
