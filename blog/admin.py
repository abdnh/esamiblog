from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post, Category, User, Comment


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'حقول إضافية',
            {
                'fields': (
                    'bio',
                    'profile_picture',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'writer')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'writer', 'post')

