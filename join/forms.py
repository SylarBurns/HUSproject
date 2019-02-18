
# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-
from django import forms
from heart.models import User

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'nickName', 'studentId', 'sex', 'birthDate', 'phone', 'email', 'icon']


        error_messages = {
            'nickName': {
                'unique': "이미 있는 닉네임입니다."
            },
            'birthDate':{
                'invalid':"[YYYY-MM-DD] 형식으로 작성하세요."
            },
            'sex':{
                'required':"성별을 선택하세요."
            },
            'icon':{
                'required':"아이콘을 선택하세요"
            }
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['birthDate'].widget.attrs['placeholder'] = "YYYY-MM-DD"