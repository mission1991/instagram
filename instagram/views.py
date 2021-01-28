from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from accounts.models import User
from .forms import PostForm, CommentForm
from .models import Post, Comment


# def search(request):
#     kw = request.GET.get('kw', '')  # 검색어
#     if kw:
#         post_list = Post.objects.filter(
#             Q(author__username__icontains=kw) |  # 작성자 검색
#             Q(tag_set__icontains=kw) |  # 태그 검색
#             Q(caption__icontains=kw) |  # 내용검색
#             Q(location__icontains=kw)  # 지역검색
#         ).distinct()
#     return render(request, 'instagram/search.html', {
#         'post_list': post_list,
#         'kw': kw
#     })

@login_required
def index(request):
    timesince = timezone.now() - timedelta(days=30)
    post_list = Post.objects.all() \
        .filter(
        Q(author=request.user) |
        Q(author__in=request.user.following_set.all())
    ) \
        .filter(
        created_at__gte=timesince
    )
    suggested_user_list = get_user_model().objects.all() \
                              .exclude(pk=request.user.pk) \
                              .exclude(pk__in=request.user.following_set.all())[:5]

    comment_form = CommentForm()

    return render(request, "instagram/index.html", {
        "post_list": post_list,
        "suggested_user_list": suggested_user_list,
        "comment_form": comment_form,
    })


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(request, "instagram/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
    })


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, "포스팅을 저장했습니다.")
            return redirect('/')
    else:
        form = PostForm()

    return render(request, "instagram/post_form.html", {
        "form": form,
    })


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('/')
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            return redirect(post)
    else:
        form = PostForm(instance=post)
    return render(request, 'instagram/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        post.delete()
    return redirect('/')


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"포스팅#{post.pk}를 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"포스팅#{post.pk} 좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.is_ajax():
                return render(request, "instagram/_comment.html", {
                    "comment": comment,
                })
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "instagram/comment_form.html", {
        "form": form,
    })


@login_required
def comment_delete(request, pk):
    commnet = get_object_or_404(Comment, pk=pk)
    if request.user != commnet.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        commnet.delete()
    return redirect('/')


@login_required
def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username)
    post_list = Post.objects.filter(author=page_user)
    follower_list = page_user.follower_set.all()
    following_list = page_user.following_set.all()
    post_list_count = post_list.count()  # 실제 데이터베이스에 count 쿼리를 던지게 됨
    follower_count = follower_list.count()
    following_count = following_list.count()

    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
        "post_list_count": post_list_count,
        "is_follow": is_follow,
        "follower_count": follower_count,
        "following_count": following_count,
    })


@login_required
def follower_list(request, username):
    follow_user = get_object_or_404(User, username=username)
    follower_all = follow_user.follower_set.all()
    return render(request, "instagram/follower_list.html", {
        "follower_all": follower_all,
    })


@login_required
def following_list(request, username):
    follow_user = get_object_or_404(User, username=username)
    following_all = follow_user.following_set.all()
    return render(request, "instagram/following_list.html", {
        "following_all": following_all,
    })