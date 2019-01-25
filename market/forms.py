from django import forms

from heart.models import Post

class marketModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =[
            'title',
            'postEditor',
            'MboardType',
            'MitemType',
            'price',
        ]
