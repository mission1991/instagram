import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))

# 장고에 빼기 필터가 없어서 따로 필터를 만듦
# |add:-3은 인수에만 적용 가능 (변수에 불가능)