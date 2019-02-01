from django.forms import ModelForm
from django.forms.widgets import RadioSelect

from heart.models import (
    Post
)

from django import forms

class lostAndFoundPostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'LFboardType',
            'title',
            'LFitemType',
            'postEditor',
        ]
        widgets = {
            'LFboardType' : RadioSelect(),
            'LFitemType' : RadioSelect()
        }


# 삭제를 위한 폼 (삭제를 위한 임의 필드)
class lostAndFoundPostDeleteForm(forms.Form):
    exist = forms.BooleanField()