from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),  # posts アプリケーションの URL を含む
    path('posts/', include('posts.urls')),  # posts アプリケーションの URL を含む
    path('users/', include('users.urls')),  
# users アプリケーションの URL を含む
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # メディアファイルのURL設定
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)