
# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-
from django import forms
from django.utils import timezone
from heart.models import User
from django.forms.widgets import Select, TextInput, FileInput

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['nickName','phone']

 
        error_messages = {
            'nickName': {
                'unique': "이미 있는 닉네임입니다."
            },
            'phone':{
                'required': "xxx-xxxx-xxxx형식으로 작성하세요"
            }
        }
