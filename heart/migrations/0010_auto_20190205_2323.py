# Generated by Django 2.1.5 on 2019-02-05 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0009_remove_comment_commenteditor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='belongToComment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subComments', to='heart.Comment'),
        ),
    ]
