from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', views.signup, name='signup'),  # サインアップページ
    path('login/', views.login_view, name='login'),  # サインインページ
    path('logout/', views.logout_view, name='logout'),  # ログアウトページ
    path('profile/', views.profile, name='profile'),  # プロフィールページ
    path('profile/<str:username>/', views.profile, name='profile'),  # ユーザーページのURLパターン
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # プロフィールページの編集ページ
    path('favorite_list/', views.favorite_list, name='favorite_list'), # お気に入り投稿ページ
    # 他のユーザー関連のURLを追加することができます
]


# メディアファイルのURL設定
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

