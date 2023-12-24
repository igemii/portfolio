from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import get_object_or_404
from .models import Post
from .models import Profile, Post
from django.contrib.auth.models import User

"""新規登録（signup）のビュー"""

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 新規登録後にログインページにリダイレクト
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



"""ログイン（login_view）のビュー"""

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # ログイン後にプロフィールページにリダイレクト
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



"""ログアウト（logout_view）のビュー"""

def logout_view(request):
    logout(request)
    return redirect('post_list')  # ログアウト後にログインページにリダイレクト



"""プロフィール（profile）のビュー"""

@login_required
def profile(request, username=None):
    if username:  # もしusernameが指定されていれば、そのユーザーのプロフィールを表示
        user = get_object_or_404(User, username=username)
        user_profile = Profile.objects.filter(user=user).first()
        user_posts = user.posts.all()
    else:  # もしusernameが指定されていなければ、ログインユーザーのプロフィールを表示
        user_profile = Profile.objects.filter(user=request.user).first()
        user_posts = request.user.posts.all()

    return render(request, 'users/profile.html', {'profile': user_profile, 'user_posts': user_posts})
# def profile(request):
#     try:
#         profile = Profile.objects.get(user=request.user)
#         user_posts = Post.objects.filter(author=request.user)
#     except Profile.DoesNotExist:
#         profile = None
#         user_posts = None
    
#     return render(request, 'users/profile.html', {'profile': profile, 'user_posts': user_posts})

def user_posts(request, user_id):
    # ユーザーのプロフィールを取得
    user_profile = Profile.objects.get(user_id=user_id)

    # ユーザーが投稿した記事を取得
    user_posts = Post.objects.filter(author=user_profile.user)

    return render(request, 'user_posts.html', {'user_profile': user_profile, 'user_posts': user_posts})



@login_required
def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user  # ユーザーIDをセットする
            form.save()
            return redirect('profile')  # 保存後、profileページにリダイレクト
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})





@login_required
def view_profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None

    return render(request, 'users/view_profile.html', {'profile': user_profile})


# @login_required #プロフィール表示
# def view_profile(request):
#     profile = Profile.objects.get_or_create(user=request.user)
#     return render(request, 'users/view_profile.html', {'profile': profile})

def profile_view(request): #profileにpost_createで投稿した内容を表示
    user = request.user
    posts = Post.objects.filter(author=user)  # ログインユーザーが作成した投稿を取得

    profile = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'users/profile.html', {'profile': profile})



"""お気に入り投稿表示"""

def display_favorite_list(request):
    current_user_profile = Profile.objects.get(user=request.user)
    favorite_posts = current_user_profile.favorite_posts.all()
    return render(request, 'favorite_list.html', {'favorite_posts': favorite_posts})

def favorite_list(request):
    # ログインユーザーのお気に入り投稿を取得
    favorite_posts = request.user.favorite_posts.all()[:5]  # 最初の5つのお気に入り投稿を取得する例

    return render(request, 'favorite_list.html', {'favorite_posts': favorite_posts})