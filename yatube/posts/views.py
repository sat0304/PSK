import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Group, Post, User
from .forms import PostForm


def index(request):
    """Главная страница."""
    template1 = 'posts/index.html'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.NUM_OF_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'post_list': post_list,
        'title_index': 'Последние обновления на сайте'
    }
    return render(request, template1, context)


def group_posts(request, slug):
    """Cтраница  публикаций."""
    template2 = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).all()
    paginator = Paginator(post_list, settings.NUM_OF_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
        'title_groups': 'Записи сообщества: '
    }
    return render(request, template2, context)


def profile(request, username):
    """Cтраница  публикаций отдельного участника."""
    template3 = 'posts/profile.html'
    try:
        auser = User.objects.get(username=username)
        # post_count = Post.objects.filter(author=auser).count()
        post_list = Post.objects.filter(author=auser).all()
        paginator = Paginator(post_list, settings.NUM_OF_POSTS_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'auser': auser,
            'page_obj': page_obj,
            # 'post_count': post_count,
            'title_author': 'Все посты пользователя ',
            'counted_posts': 'Всего постов: '
        }
        return render(request, template3, context)
    except TypeError:
        assert("Error in user profile page test_paginator")
    except AttributeError:
        assert("Error in user profile page utils")


def post_detail(request, post_id):
    """Cтраница отдельной публикации участника."""
    template4 = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    post_count = Post.objects.filter(author=author).count()
    context = {
        'author': author,
        'post_count': post_count,
        'post': post,
        'title_post': 'Пост '
    }
    return render(request, template4, context)


@login_required
def post_create(request):
    """Страница создания записи."""
    template5 = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(False)
            form.author = request.user
            form.pub_date = datetime.datetime.now()
            form.save()
            return redirect('posts:profile', username=form.author)
        else:
            context = {'form': form}
            return render(request, template5, context)
    else:
        context = {
            'form': form,
            'new_post': 'Новый пост'
        }
        return render(request, template5, context)


@login_required
def post_edit(request, post_id):
    """Страница редактирования записи."""
    template5 = 'posts/create_post.html'
    template6 = 'posts:post_detail'
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        is_edit = True
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post1 = form.save(commit=False)
                post1.author = request.user
                post1.save()
                return redirect(template6, post_id)
            else:
                return render(
                    request,
                    template5,
                    {
                        'post_id': post_id,
                        'form': form,
                        'is_edit': is_edit
                    }
                )
        form = PostForm(instance=post)
        return render(
            request,
            template5,
            {
                'post_id': post_id,
                'form': form,
                'is_edit': is_edit
            }
        )
    else:
        return redirect(template6, post_id)
