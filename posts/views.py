from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PostForm  # PostForm を作成する必要があります
from .models import Post, Comment
from .forms import CommentForm
from .models import Comment
from .models import Favorite
from django.db.models import Count
from django.urls import reverse



"""投稿一覧のビュー"""

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




"""投稿詳細のビュー"""

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # 投稿を取得するクエリ
    return render(request, 'posts/post_detail.html', {'post': post})



"""新規投稿のビュー"""

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # フォームが有効な場合、commit=False でフォームの内容を保存してから
            # author フィールドを現在のログインユーザーに設定し、保存する
            post = form.save(commit=False)
            post.author = request.user  # 現在のログインユーザーを author として設定
            post.save()
            return redirect('post_detail', pk=post.pk)  # 投稿作成後に post_detail ページにリダイレクト
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})



"""投稿削除のビュー"""

def delete_post(request, post_id):
    # POST メソッドの場合のみ削除を処理する
    if request.method == 'POST':
        # 削除対象の投稿を取得
        post = get_object_or_404(Post, pk=post_id)
        
        # 投稿を削除するための権限チェック
        if request.user == post.author:  # ログインユーザーが投稿者かどうかチェック
            post.delete()
            # 削除が完了したらリダイレクトする（適切なURLに置き換える）
            return redirect('post_list')
        else:
            # 投稿者でない場合は何らかのエラーを返すか、リダイレクトする
            # 例： return redirect('post_detail', post_id=post_id)
            pass

    # POST メソッドでない場合や、削除権限がない場合の処理
    # 例えば詳細ページにリダイレクトするなど
    return redirect('post_detail', post_id=post_id)





"""コメント追加のビュー"""

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # コメントの作者をログインユーザーに設定
            comment.save()
            return redirect('post_detail', pk=post.pk)  # 投稿詳細ページにリダイレクト
    else:
        form = CommentForm()
    return render(request, 'posts/add_comment_to_post.html', {'form': form})




"""コメント削除のビュー"""

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_pk = comment.post.pk  # コメントが属する投稿の pk を取得
    if request.user == comment.author:
        comment.delete()
    return redirect('post_detail', pk=post_pk)



"""いいね！登録のビュー"""

def like_post(request, post_id):
    # ここにいいねのロジックを追加する
    # ...
    return redirect('post_detail', pk=post_id)  # リダイレクト先である投稿詳細ページに post_id を渡してリダイレクトする





"""お気に入り登録のビュー"""
def favorite_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # お気に入り登録がすでにされているか確認
    if Favorite.objects.filter(user=request.user, post=post).exists():
        # お気に入り登録がすでにされている場合の処理
        pass
    else:
        # お気に入り登録を行う場合の処理
        favorite = Favorite(user=request.user, post=post)
        favorite.save()

    # お気に入り登録後、リダイレクト先などの処理を行う
    return redirect('post_detail', pk=post_id)  # pk=post_id として修正



"""検索ビュー"""

def search_posts(request):
    query = request.GET.get('q')
    if query:
        # タイトルまたは説明に検索クエリが部分一致する投稿をフィルタリング
        posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(description__icontains=query)
    else:
        # クエリが提供されていない場合は全ての投稿を表示
        posts = Post.objects.all()
    
    return render(request, 'posts/post_list.html', {'posts': posts})