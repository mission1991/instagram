from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.core.paginator import Paginator

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-created')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-created')
    else:  # recent
        question_list = Question.objects.order_by('-created')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답글 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    return render(request, 'comm/question_list.html', {
        'question_list': page_obj,
        'page': page,
        'kw': kw,
        'so': so
    })


def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'comm/question_detail.html', {
        'question': question,
    })


#  질문 기능
@login_required(login_url='accounts:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('comm:index')
    form = QuestionForm()
    return render(request, 'comm/question_form.html', {
        'form': form
    })


@login_required(login_url='accounts:login')
def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect(question)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect(question)
    else:
        form = QuestionForm(instance=question)
    return render(request, "comm/question_form.html", {
        'form': form
    })


@login_required(login_url='accounts:login')
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('comm:detail', pk)
    question.delete()
    return redirect('comm:index')


# 답변 기능
@login_required(login_url='accounts:login')
def answer_create(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            # return redirect('comm:detail', pk)
            return redirect('{}#answer_{}'.format(
            resolve_url(question), pk))
    else:
        form = AnswerForm()
    return render(request, 'comm/question_detail.html', {
        'question': question,
        'form': form
    })


@login_required(login_url='accounts:login')
def answer_update(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('comm:detail', pk=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.save()
            # return redirect('comm:detail', pk=answer.question.id)
            return redirect('{}#answer_{}'.format(
                resolve_url('comm:detail', pk=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'comm/answer_form.html', {
        'answer': answer,
        'form': form
    })


@login_required(login_url='accounts:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('comm:detail', pk=answer.question.id)


# 추천 기능
@login_required(login_url='accounts:login')
def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect(question)


@login_required(login_url='accounts:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question = get_object_or_404(Question, pk=answer.question.id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect(question)


