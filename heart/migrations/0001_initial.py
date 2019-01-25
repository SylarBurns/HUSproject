# Generated by Django 2.1.3 on 2019-01-25 04:21

import ckeditor_uploader.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=20)),
                ('nickName', models.CharField(max_length=20, unique=True)),
                ('studentId', models.PositiveIntegerField(default=None, null=True)),
                ('sex', models.CharField(max_length=1)),
                ('birthDate', models.DateField(blank=True, default=None, null=True)),
                ('phone', models.CharField(default=None, max_length=15, null=True)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('pubDate', models.DateTimeField(auto_now_add=True)),
                ('commentEditor', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('belongToComment', models.PositiveIntegerField(blank=True)),
                ('stance', models.PositiveIntegerField(blank=True)),
                ('reportStatus', models.CharField(blank=True, max_length=10)),
                ('noticeChecked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ComRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annonimity', models.BooleanField(default=False)),
                ('annoName', models.CharField(blank=True, max_length=20)),
                ('isWriter', models.BooleanField(default=False)),
                ('like', models.BooleanField(default=False)),
                ('dislike', models.BooleanField(default=False)),
                ('vote', models.PositiveIntegerField(blank=True, null=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='com_relation', to='heart.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='com_relation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='제목')),
                ('postEditor', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='내용')),
                ('pubDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now_add=True)),
                ('hitCount', models.PositiveIntegerField(default=0)),
                ('boardNum', models.PositiveIntegerField()),
                ('reportStatus', models.CharField(blank=True, max_length=10)),
                ('status', models.CharField(blank=True, max_length=10)),
                ('LFboardType', models.CharField(choices=[('Lost', 'LOST'), ('Found', 'FOUND')], default='Lost', max_length=10)),
                ('MboardType', models.CharField(choices=[('Lost', 'LOST'), ('Found', 'FOUND')], default='Lost', max_length=10)),
                ('LFitemType', models.CharField(choices=[('idcard', '학생증'), ('electronic', '전자기기'), ('cash', '돈/카드/지갑'), ('etc', '기타')], default='idcard', max_length=10)),
                ('MitemType', models.CharField(choices=[('idcard', '학생증'), ('electronic', '전자기기'), ('cash', '돈/카드/지갑'), ('etc', '기타')], default='idcard', max_length=10)),
                ('price', models.CharField(blank=True, max_length=100)),
                ('exist', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annonimity', models.BooleanField(default=False)),
                ('annoName', models.CharField(blank=True, max_length=20)),
                ('isWriter', models.BooleanField(default=False)),
                ('like', models.BooleanField(default=False)),
                ('dislike', models.BooleanField(default=False)),
                ('vote', models.PositiveIntegerField(blank=True, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_relation', to='heart.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_relation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='users',
            field=models.ManyToManyField(through='heart.PostRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='file',
            name='belongTo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heart.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='heart.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='users',
            field=models.ManyToManyField(through='heart.ComRelation', to=settings.AUTH_USER_MODEL),
        ),
    ]
