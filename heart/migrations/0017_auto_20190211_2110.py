# Generated by Django 2.1.5 on 2019-02-11 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0016_auto_20190211_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reportResult',
            field=models.TextField(blank=True, max_length=500, verbose_name='신고처리결과'),
        ),
        migrations.AlterField(
            model_name='post',
            name='reportResult',
            field=models.TextField(blank=True, max_length=500, verbose_name='신고처리결과'),
        ),
    ]