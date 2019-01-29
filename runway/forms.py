from django.forms import ModelForm, BooleanField
from django.forms.widgets import RadioSelect
from django import forms
from heart.models import Post
from heart.models import PostRelation

class PostModelForm(ModelForm):
    #익명성 표기를 위한 추가 필드 생성
    ANO_CHOICES = [('nickName', '닉네임'), ('annonimity', '익명')]
    annonimity = forms.ChoiceField(
        label = '표기',
        widget = forms.RadioSelect(),
        choices = ANO_CHOICES
    )

    class Meta:
        model = Post
        fields = ['title','RWboardType', 'annonimity', 'postEditor', ]
        widgets = {
            'RWboardType': RadioSelect()
        }

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
