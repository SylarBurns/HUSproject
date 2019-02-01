from django.forms import ModelForm
from django.forms.widgets import RadioSelect

from heart.models import (
    Post
)

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