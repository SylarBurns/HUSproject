# Generated by Django 2.1.3 on 2019-01-31 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0007_auto_20190131_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='belongToComment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subComments', to='heart.Comment'),
        ),
    ]