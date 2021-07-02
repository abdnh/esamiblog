from django.contrib.syndication.views import Feed
from blog.models import Post, User

class LatestPostsFeed(Feed):
    title = "عصامي بلوغ"
    link = "/posts/"
    description = "آخر المنشورات في عصامي بلوغ."

    def items(self):
        return Post.objects.order_by('-created')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        content = str(item.content)
        if len(content) > 30:
            content = content[:30] + '…'
        else:
            content = content[:30]
        return content

class UserPostsFeed(Feed):

    def get_object(self, request, username):
        return User.objects.get(username=username)

    def title(self, obj):
        return f'آخر منشورات {obj.username} في عصامي بلوغ'

    def description(self, obj):
        return self.title(obj)

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self, obj):
        return Post.objects.filter(writer=obj).order_by('-created')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        content = str(item.content)
        if len(content) > 30:
            content = content[:30] + '…'
        else:
            content = content[:30]
        return content
