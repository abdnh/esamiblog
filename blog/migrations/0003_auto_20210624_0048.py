# Generated by Django 3.2.4 on 2021-06-23 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='pub_date',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='commenter',
        ),
        migrations.AddField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='كاتب'),
        ),
    ]
