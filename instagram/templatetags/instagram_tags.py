from django import template

register = template.Library()


@register.filter
def is_like_user(post, user):
    return post.is_like_user(user)

#템플릿에서 함수 사용하려고 커스텀 템플릿 구현