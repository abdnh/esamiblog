# Generated by Django 3.2.4 on 2021-07-02 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'هذا البريد الإلكتروني مستخدم بالفعل.'}, max_length=254, unique=True, verbose_name='بريد إلكتروني'),
        ),
    ]
