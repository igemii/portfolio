from django import forms
from .models import Post
from .models import Comment

"""投稿フォーム"""

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'images']  # 'images' フィールドを指定
      
      
        
        



"""コメントフォーム"""

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # コメントのテキストフィールドを指定

