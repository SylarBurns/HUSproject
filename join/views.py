#-*-coding:utf-8
import requests, json
#import json
from bs4 import BeautifulSoup as bs
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from heart.models import User
from django.contrib.auth import login as auth_login
from django.views import generic
from .forms import UserForm
from django.contrib import messages
'''
1. 크롤링 하기 위해 다음 두가지 설치 필요
pip install requests
pip install beautifulsoup4
2. 로직
 1) 히즈넷 로그인 시도
 2) 히즈넷의 학번과 db의 학번 비교
    a) 같다면, 한우리 로그인
    b) 아닐 경우, 회원가입 (User 등록)
'''

def check(request):
    username = request.POST["username"]
    password = request.POST["password"]

    try:
        getStudentId = hisnetCheck("login", username, password)
        try:                 # 한우리 로그인 성공
            user = User.objects.exclude(is_active = False).get(studentId = getStudentId)
            auth_login(request, user)
            return redirect('mainPage:mainPage')

        except:              # 회원가입 ( 히즈넷 로그인 성공 & 한우리 회원가입 안된 상태)
            getInform = hisnetCheck("register", username, password)
            request.session['data'] = getInform
            #return renderSignUp(request, getInform)
            return redirect('join:clause')

    except:       # 히즈넷 로그인 실패 --> TODO: 경고창 띄우기  
        return LoginError(request)



def hisnetCheck(use, user_id, user_pw):
    LOGIN_INFO = {
		'id': str(user_id),
		'password': str(user_pw)
	}	
    with requests.Session() as s:
		#print(json.dumps(LOGIN_INFO).encode('utf-8')))
        login_req = s.post('https://hisnet.handong.edu/login/_login.php', data=LOGIN_INFO)
        if login_req.status_code != 200:
            raise Exception('ID or password is wrong. Try again.')
        post = s.get('https://hisnet.handong.edu/haksa/hakjuk/HHAK110M.php')
        soup = bs(post.text, 'html.parser')
        try:
            studentID = soup.find('input',{'name':'hakbun'})['value']
            email= soup.find('input',{'name':'hakj_email'})['value']
            phone = soup.find('input',{'name':'hakj_hak_pager'})['value']
			#이거는 특징이 없어서 무식하게 했다. html자체가 무식하게 짜여져 있기 때문이다.
            korName = soup.find_all('table')[8].find_all('td')[1].get_text()
        except:
            #교직원은 php문서가 달라서 따로 처리해야된다
            post = s.get('https://hisnet.handong.edu/prof/basic/PBAS001M.php')
            soup = bs(post.text, 'html.parser')
            studentID = soup.find('input',{'name':'UserID'})['value']
            email= soup.find('input',{'name':'kich_email'})['value']
            phone = soup.find('input',{'name':'kich_tel2'})['value']
            korName = soup.find('input',{'name':'UserName'})['value']
        if(use is "login"):
            return studentID
        elif(use is "register"):
            userInform = {"studentID":studentID, "email":email, "korName":korName, "phone":phone}
            return userInform
class SignUpView(generic.View):

    form_class = UserForm
    template_name = "join/register.html"

    def get(self, request, *args, **kwargs):
        form = UserForm()
        userInfo = request.session.get('data')
        args = {'form':form, 'data':userInfo}
        return render(request, 'join/register.html', args)

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        userInfo = request.session.get('data')
        args = {'form':form, 'data':userInfo}
        if form.is_valid():
            KorName = form.cleaned_data["name"]
            StudentID = form.cleaned_data["studentId"]
            NickName = form.cleaned_data["nickName"]
            BirthDate = form.cleaned_data["birthDate"]
            Phone = form.cleaned_data["phone"]
            Sex = form.cleaned_data["sex"]
            Email = form.cleaned_data["email"]
            
            user = User.objects.create_user(username = str(StudentID)+'hgu', password = "Qkfrksakt206", name = KorName, nickName =  NickName, studentId = StudentID, sex = Sex, email = Email, phone = Phone, birthDate = BirthDate)
            auth_login(request, user)
            return redirect('mainPage:mainPage')
        else:  
            return render(request, 'join/register.html', args)
    
class ClauseView(generic.TemplateView):
    template_name = 'join/clause.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, 'join/clause.html')

    def post(self, request, *args, **kwargs):
        isAgree = request.POST.get("check")
        if isAgree == "agree":
            return redirect("join:signup")
        else:
            messages.warning(request, '동의하셔야 회원가입을 할 수 있습니다.')
            return render(request, 'join/clause.html')
        

def LoginError(request):
	return render(request,'join/login_error.html')
