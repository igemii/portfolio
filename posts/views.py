import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, Comment, Favorite, PostImage

# 投稿一覧のビュー
def post_list(request):
    sort_option = request.GET.get('sort')

    if sort_option == 'latest':
        posts = Post.objects.order_by('-created_at')
    elif sort_option == 'oldest':
        posts = Post.objects.order_by('created_at')
    elif sort_option == 'most_liked':
        posts = Post.objects.annotate(likes_count=Count('favorite')).order_by('-likes_count')
    elif sort_option == 'most_favorited':
        posts = Post.objects.annotate(favorites_count=Count('favorite')).order_by('-favorites_count')
    else:
        posts = Post.objects.all()

    return render(request, 'posts/post_list.html', {'posts': posts})

# 投稿詳細のビュー
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

# 新規投稿のビュー
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            images = request.FILES.getlist('images')
            for image in images:
                post_image = PostImage.objects.create(image=image)
                post.images.add(post_image)
            
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})

# 投稿編集のビュー
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST' and request.user == post.author:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            delete_image = request.POST.get('delete_image')
            if delete_image == 'delete':
                if post.image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(post.image)))
                    post.image = None
            form.save()
            return redirect('post_detail', pk=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})

# 投稿削除のビュー
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST' and request.user == post.author:
        post.delete()
        messages.success(request, '投稿が削除されました')
        return redirect('post_list')
    else:
        messages.error(request, '投稿を削除できませんでした')
        return redirect('post_detail', pk=post_id)

# コメント追加のビュー
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/add_comment_to_post.html', {'form': form})

# コメント削除のビュー
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_pk = comment.post.pk
    if request.user == comment.author:
        comment.delete()
    return redirect('post_detail', pk=post_pk)

# いいね！登録のビュー
def like_post(request, post_id):
    return redirect('post_detail', pk=post_id)

# お気に入り登録のビュー
def favorite_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not Favorite.objects.filter(user=request.user, post=post).exists():
        favorite = Favorite(user=request.user, post=post)
        favorite.save()

    return redirect('post_detail', pk=post_id)

# 検索ビュー
def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(description__icontains=query)
    else:
        posts = Post.objects.all()
    
    return render(request, 'posts/post_list.html', {'posts': posts})
