from django import forms
from heart.models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'postEditor')

# class CommentForm(forms.ModelForm):
    
#     class Meta:
#         model = Comment
#         fields = ('title', 'content')
