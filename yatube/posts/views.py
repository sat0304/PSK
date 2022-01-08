import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from .models import Group, Follow, Post, User
from .forms import CommentForm, PostForm


@cache_page(20)
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
    auser = User.objects.get(username=username)
    template3 = 'posts/profile.html'
    post_list = Post.objects.filter(author=auser).all()
    paginator = Paginator(post_list, settings.NUM_OF_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        following1 = False
        follow = Follow.objects.filter(user=request.user)
        following_author = User.objects.filter(following__in=follow)
        for name in following_author:
            if username in name.username:
                following1 = True
            else:
                following1 = False
        context = {
            'auser': auser,
            'page_obj': page_obj,
            'title_author': 'Все посты пользователя ',
            'counted_posts': 'Всего постов: ',
            'following1': following1,
        }
        return render(request, template3, context)
    else:
        return redirect('posts:index')  


def post_detail(request, post_id):
    """Cтраница отдельной публикации участника."""
    template4 = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    comments = post.comments.all()
    form = CommentForm(request.POST)
    context = {
        'author': author,
        'post': post,
        'comments': comments,
        'form': form,
        'title_post': 'Пост '
    }
    return render(request, template4, context)


@login_required
def post_create(request):
    """Страница создания записи."""
    template5 = 'posts/create_post.html'
    form = PostForm(
        request.POST or None, 
        files=request.FILES or None
    )
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
            form = PostForm(
                request.POST,
                instance=post,
                files=request.FILES or None
            )
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


@login_required
def add_comment(request, post_id):
    """Страница поста с комментариями."""
    template7 = 'posts:post_detail'
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect(template7, post_id=post_id)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, template7, context)


@login_required
def follow_index(request):
    """Страница постов по подписке на авторов."""
    template8 = 'posts/follow.html'
    follow = Follow.objects.filter(user=request.user)
    following_author = User.objects.filter(following__in=follow)
    post_list = Post.objects.filter(author__in=following_author)
    paginator = Paginator(post_list, settings.NUM_OF_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title_follow': 'Последние обновления по подписке',
    }
    return render(request, template8, context)


@login_required
def profile_follow(request, username):
    """Функция подписки на автора."""
    template9 = 'posts:profile'
    auser = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        author=auser).filter(
            user=request.user.is_authenticated).count()
    if request.user != auser:
        if follow == 0:
            Follow.objects.create(
                user=request.user,
                author=auser)
        return redirect(template9, username=username)
    return redirect(template9, username=username)


@login_required
def profile_unfollow(request, username):
    """Функция удаления подписки на автора."""
    template9 = 'posts:profile'
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(
        user=request.user,
        author=author
    ).delete()
    return redirect(template9, username=username)
