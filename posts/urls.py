from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # トップページ用のURLパターン
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # 投稿詳細ページ
    path('post/new/', views.post_create, name='post_create'),  # 新しい投稿作成ページ
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),  # コメント追加ページ
    path('posts/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),  # コメント削除ページ
    path('like/<int:post_id>/', views.like_post, name='like_post'), #いいね！登録
    path('posts/favorite/<int:post_id>/', views.favorite_post, name='favorite_post'), # お気に入り登録のためのURLパターン
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'), #投稿削除
    path('posts/search/', views.search_posts, name='search_posts'),  #  検索ページ
    # 他の必要なパスやビューを追加することができます
]


