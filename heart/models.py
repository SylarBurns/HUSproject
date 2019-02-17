from django.db import models
from django.utils.timezone import datetime
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.
# -*- coding: utf-8 -*-
class User(AbstractUser):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=20)#사용자의 이름
    nickName=models.CharField(max_length=20, unique = True, null=False)#사용자가 설정한 닉네임#사용자가 설정한 닉네임
    studentId=models.PositiveIntegerField(null=True, default=None)#학번;
    sex=models.CharField(max_length=1)#성별; 남자 : M, 여자 : F
    birthDate=models.DateField(null=True, blank = True, default=None)#생일; 형식 : 1995-09-30
    icon=models.CharField(max_length = 50, null=True, default=None)#사용자가 가입할 때 선택할 수 있는 아이콘
    
    phone=models.CharField(max_length=15, null=True, default=None)#핸드폰 번호; 형식: xxx-xxxx-xxxx
    # blockUser=ListCharField(
    #     base_field=IntegerField(max_length=10),
    #     size=100,
    #     max_length=(7 * 100),
    #     blank=True
    # )
    # 사용자가 차단한 유저의 정보; pk로 저장하고 최대치는 100명으로 설정함
    email=models.EmailField(default=None)#사용자의 이메일 정보
    objects = UserManager()
    def delete(self):
        self.is_active = False
        self.save()

class Post(models.Model):
    BOARD_CHOICES = (
        ('Lost','LOST'),('Found','FOUND')
    )
    
    ITEM_CHOICES = (
        ('idcard','학생증'),('electronic','전자기기'),('cash','돈/카드/지갑'),('etc','기타'),
    )
    BOARD_CHOICES_MARKET = (
        ('sell','팝니다'),('buy','삽니다')
    )
    ITEM_CHOICES_MARKET = (
        ('book','책'),('cloth','옷'),('electronics','전자기기'),('lifeItems','생활용품'),('house','집'),('job','구인구직'),('cosmetics','화장품'),('etc','기타')
    )
    BOARD_CHOICES_RUNWAY = (
        ('Argument','찬반토론'), ('General','일반토론')
    )

    title = models.CharField("제목", max_length=100, blank=False)
    writer = models.CharField("작성자", max_length=20, blank=False, null=True) 
    # content = models.CharField(max_length=3000, blank= True)
    postEditor =  RichTextUploadingField("내용", blank=True, null=True,
                                          external_plugin_resources=[(
                                          'youtube',
                                          '/static/heart/external/ckeditor_plugins/youtube/youtube/',
                                          'plugin.js',
                                          )],
                                      )
    pubDate = models.DateTimeField(auto_now_add=True, blank=False) 
    updateDate = models.DateTimeField(auto_now_add=True, blank=True) 
    hitCount = models.PositiveIntegerField(default=0) #조회수
    boardNum = models.PositiveIntegerField(blank=False) #게시판 별 고유번호
    reportStatus = models.CharField(max_length=10, blank=True) # mypage-신고내역 ( 미확인, 확인중, 확인완료 )
    status = models.CharField(max_length=10, blank=True)  # lostNfound, 한동장터 ( 판매중, 판매완료, Lost, Found, 해결완료 )
    LFboardType = models.CharField(choices=BOARD_CHOICES, max_length=10, default='Lost') # lostNfound( Lost, Found )
    MboardType = models.CharField(choices=BOARD_CHOICES_MARKET, max_length=10, default='Lost') # 한동장터 ( 팝니다, 삽니다)
    LFitemType = models.CharField(choices=ITEM_CHOICES, max_length=10, default='idcard') #lostNfound( 태그 )
    MitemType = models.CharField(choices=ITEM_CHOICES_MARKET, max_length=10, default='idcard') # 한동장터 ( 태그 )
    RWboardType = models.CharField(choices=BOARD_CHOICES_RUNWAY, max_length=10, default='찬반토론') # 활주로 (찬반토론, 일반토론)
    price = models.CharField(max_length=100, blank=True) 
    exist = models.BooleanField(default=True) # 삭제 여부
    reportResult = models.TextField(max_length=500, verbose_name='신고처리결과', blank=True) #신고된 게시글의 처리 결과
    users = models.ManyToManyField(
      User,
      through = 'PostRelation',
      through_fields = ('post', 'user'),
    )

    def __str__(self):
        return self.title
    
    def update_hitCount(self):
        self.hitCount += 1
        self.save()
        return self.hitCount

    def forCount(self):
        return self.post_relation.filter(vote=1).count()
    
    def againstCount(self):
        return self.post_relation.filter(vote=0).count()

    def neutralCount(self):
        return self.post_relation.filter(vote=2).count()
    
    def likeCount(self):
        return self.post_relation.filter(like=True).count()

    def dislikeCount(self):
        return self.post_relation.filter(dislike=True).count()

    def getWriter(self):
        relation = self.post_relation.filter(isWriter=True).get()
        return relation.user

    def getWriterRelation(self):
        relation = self.post_relation.filter(isWriter=True).get()
        return relation

    def getScorePlus(self):
        score = (((self.likeCount+self.dislikeCount)/self.hitCount)*100)+self.hitCount
        return score
    
    def getScoreMinus(self):
        score = (((self.likeCount-self.dislikeCount)/self.hitCount)*100)+self.hitCount
        return score

    def getScoreRW(self):
        score = (((self.forCount+self.againstCount+self.neutralCount)/self.hitCount)*100)+self.hitCount
        return score
    def was_published_recently(self):
        return self.pubDate >= timezone.now() - datetime.timedelta(days=1)

class Comment(models.Model):
    title = models.CharField(max_length=100, blank=True)  #활주로에서 댓글이 게시글 형식으로 달릴 때 필요
    writer = models.CharField("작성자", max_length=20, blank=False, null=True)     
    users = models.ManyToManyField(
        User, 
        through='ComRelation',
        through_fields=('comment', 'user'))  #댓글과 관련된 유저들
    pubDate = models.DateTimeField(auto_now_add=True) #댓글 생성날짜
    content = models.TextField(max_length=3000, blank=True) #댓글 내용
    # commentEditor = RichTextUploadingField(blank=True, null=True, config_name='comment')
    # belongToBoard = models.PositiveIntegerField(blank= True) #어떤 게시판에 소속된 댓글인지 알 수 있도록 게시판의 pk표시
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
    belongToComment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subComments')#어떤 댓글에 소속된 대댓글인지 알 수 있도록 상위 댓글의 pk표시
    stance = models.PositiveIntegerField(null=True, blank= True) #활주로에서 댓글의 의견 상태 표시 0:반대 1:찬성 2:중립
    reportStatus = models.CharField(max_length=10,blank= True) #신고 상태
    noticeChecked = models.BooleanField(default=False) #알림을 확인 했는지 표시
    reportResult = models.TextField(max_length=500, verbose_name='신고처리결과', blank=True) #신고된 댓글의 처리 결과

   
    def __str__(self):
        return self.content
    
    def getWriter(self):
        relation = self.com_relation.filter(isWriter=True).get()
        return relation.user
    def getWriterStudentId(self):
        relation = self.com_relation.filter(isWriter=True).get()
        return relation.user.studentId

    def getWriterRelation(self):
        relation = self.com_relation.filter(isWriter=True).get()
        return relation

    def likeCount(self):
        return self.com_relation.filter(like=True).count()

    def dislikeCount(self):
        return self.com_relation.filter(dislike=True).count()

    def was_published_recently(self):
        return self.pubDate >= timezone.now() - datetime.timedelta(days=1)

class File(models.Model):
    belongTo = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)

class PostRelation(models.Model):
    annonimity=models.BooleanField(default=False)
    annoName=models.CharField(max_length=20, blank= True)
    isWriter=models.BooleanField(default=False)
    isReporter=models.BooleanField(default=False)
    like=models.BooleanField(default=False)
    dislike=models.BooleanField(default=False)
    vote=models.PositiveIntegerField(null=True, blank= True) #각 게시물 detailview에서 내가 투표한 결과를 볼 수 있게
    user = models.ForeignKey(User, related_name = 'post_relation',on_delete=models.CASCADE)#user로 연결되는 foreignkey
    post = models.ForeignKey(Post, related_name = 'post_relation', on_delete=models.CASCADE)#post로 연결되는 foreignkey
    def __str__(self):
        name = self.user.nickName + " + " + self.post.title
        return name

class ComRelation(models.Model):
    annonimity=models.BooleanField(default=False)
    annoName=models.CharField(max_length=20, blank= True)
    isWriter=models.BooleanField(default=False)
    isReporter=models.BooleanField(default=False)
    like=models.BooleanField(default=False)
    dislike=models.BooleanField(default=False)
    vote=models.PositiveIntegerField(null=True, blank= True) #각 게시물 detailview에서 내가 투표한 결과를 볼 수 있게
    user = models.ForeignKey(User, related_name = 'com_relation', on_delete=models.CASCADE)#user로 연결되는 foreignkey
    comment = models.ForeignKey(Comment, related_name = 'com_relation', on_delete=models.CASCADE)#comment로 연결되는 foreignkey