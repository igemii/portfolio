from django.contrib.auth.models import User
from django.db import models
from posts.models import Post


"""プロフィールモデル"""

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    icon = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.name
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     bio = models.TextField(blank=True)
#     icon = models.ImageField(upload_to='profile_images/', blank=True, null=True)

#     def __str__(self):
#         return self.name

"""画像のモデル"""

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return self.title if hasattr(self, 'title') else str(self.id)
# class Post(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
#     image = models.ImageField(upload_to='post_images/')

#     def __str__(self):
#         return self.title if hasattr(self, 'title') else str(self.id)

#     class Meta:
#         app_label = 'users'





# class Post(models.Model):
#     # 他の投稿モデルのフィールド
#     # ...
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
#     image = models.ImageField(upload_to='post_images/')

#     def __str__(self):
#         return self.title  # 投稿モデルに'title'フィールドがあると仮定します