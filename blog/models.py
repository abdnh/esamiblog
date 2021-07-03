from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

def user_content_path(user, filename):
    return 'usercontent/{0}/profile{1}'.format(user.id, filename[filename.rfind('.'):])

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, error_messages={
        'unique': _('This email address is already used.')
    })
    bio = models.TextField(_('about the author'), null=True, blank=True)
    profile_picture = models.ImageField(_('profile picture'), upload_to=user_content_path, null=True, blank=True)

    class Meta:
        ordering = ['username']

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'username': self.get_username()})

    def __str__(self):
        return self.get_username()


class Category(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('categories')

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(_('title'), max_length=200)  
    created = models.DateTimeField(_('publication date'), auto_now_add=True)
    mod = models.DateTimeField(_('last modification date'), auto_now=True)
    content = models.TextField(_('text'))
    writer = models.ForeignKey(User, verbose_name=_('author'), null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    created = models.DateTimeField(verbose_name=_('publication date'), auto_now_add=True)
    content = models.TextField(verbose_name=_('content'))
    writer = models.ForeignKey(User, verbose_name=_('author'), null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, verbose_name=_('parent post'), null=True, on_delete=models.SET_NULL, related_name='comments')
    parent_comment = models.ForeignKey('self', verbose_name=_('parent comment'), null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return _('comment #%(comment_id) on post "%(post_title)"') % {'comment_id': self.id, 'post_title': self.post.title}

    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['created']

