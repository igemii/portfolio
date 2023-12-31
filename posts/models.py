from django.db import models
from django.contrib.auth.models import User
# from .models import Post


"""投稿のモデル"""

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    description = models.TextField()
    images = models.ManyToManyField('PostImage', blank=True)  # PostImageモデルとの多対多のリレーションを定義

    def __str__(self):
        return self.title
    

"""投稿写真のモデル"""

class PostImage(models.Model):
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return str(self.image)


"""コメントのモデル"""

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text



"""お気に入りのモデル"""


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

    

    