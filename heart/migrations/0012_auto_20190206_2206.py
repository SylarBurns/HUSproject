# Generated by Django 2.1.5 on 2019-02-06 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0011_auto_20190206_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reportResult',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='post',
            name='reportResult',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
