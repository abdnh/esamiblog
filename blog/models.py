from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser

def user_content_path(user, filename):
    return 'usercontent/{0}/profile{1}'.format(user.id, filename[filename.rfind('.'):])

class User(AbstractUser):
    email = models.EmailField(verbose_name='بريد إلكتروني', unique=True, error_messages={
        'unique': 'هذا البريد الإلكتروني مستخدم بالفعل.'
    })
    bio = models.TextField(verbose_name='نبذة عن الكاتب', null=True, blank=True)
    profile_picture = models.ImageField(verbose_name='صورة', upload_to=user_content_path, null=True, blank=True)

    class Meta:
        ordering = ['username']

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'username': self.get_username()})

    def __str__(self):
        return self.get_username()


class Category(models.Model):
    name = models.CharField(verbose_name='اسم', max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=200)  
    created = models.DateTimeField('تاريخ النشر', auto_now_add=True)
    mod = models.DateTimeField('آخر تعديل', auto_now=True)
    content = models.TextField(verbose_name='نص')
    writer = models.ForeignKey(User, verbose_name='كاتب', null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(Category, verbose_name='مواضيع', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    created = models.DateTimeField(verbose_name='تاريخ الإنشاء', auto_now_add=True)
    content = models.TextField(verbose_name='نص التعليق')
    writer = models.ForeignKey(User, verbose_name='كاتب', null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, verbose_name='منشور', null=True, on_delete=models.SET_NULL, related_name='comments')
    parent_comment = models.ForeignKey('self', verbose_name='التعليق الأب', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'التعليق #{self.id} على منشور "{self.post.title}"'

    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['created']

