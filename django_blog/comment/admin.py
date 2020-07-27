from django.contrib import admin

from .models import Comment
from django_blog.custom_site import custom_site
from django_blog.base_admin import BaseOwnerAdmin


@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'website',
                    'email', 'status', 'created_time')
    list_display_links = ('nickname', )

    list_filter = ('target', )

