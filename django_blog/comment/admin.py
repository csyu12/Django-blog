from django.contrib import admin

from .adminforms import CommentAdminForm
from .models import Comment
from django_blog.custom_site import custom_site


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = ('target', 'nickname', 'website',
                    'email', 'status', 'created_time')
    list_display_links = ('nickname', )

    list_filter = ('target', )

