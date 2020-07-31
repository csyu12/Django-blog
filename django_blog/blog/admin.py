from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Tag, Post
from .adminforms import PostAdminForm
from django_blog.base_admin import BaseOwnerAdmin
from django_blog.custom_site import custom_site


class PostInline(admin.StackedInline):  # 样式：TabularInline, StackedInline
    fields = ('title', 'desc', 'tag', 'owner')
    extra = 1   # 控制几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]    # 在编辑分类页面，多一个编辑/新增文章的组件
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    # 注释以下代码，因为继承了BaseOwnerAdmin
    # --------------------------------- #
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)
    #
    # # 只显示作者为当前用户的分类
    # def get_queryset(self, request):
    #     qs = super(CategoryAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)
    # --------------------------------- #


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    # 注释以下代码，因为继承了BaseOwnerAdmin
    # --------------------------------- #
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)
    #
    # # 只显示作者为当前用户的标签
    # def get_queryset(self, request):
    #     qs = super(TagAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)
    # --------------------------------- #


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


# 博客主体，保留最全的admin定制
@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm    # 重新定义后台form，可以扩展更多字段定制需求
    list_display = (
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    )
    list_display_links = []

    # list_filter = ['category', 'tag']
    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # save_on_top = True    # 详情页顶部保存相关按钮

    filter_horizontal = ('tag', )   # 水平
    # filter_vertical = ('tag', )   # 垂直

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse', ),
            'fields': ('tag', ),
        }),
    )

    # 自定义编辑按钮
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     kwargs['form'] = form_factory(request.user)
    #     return super(PostAdmin, self).get_form(request, obj, change, **kwargs)


    # 注释以下代码，因为继承了BaseOwnerAdmin
    # --------------------------------- #
    # """ 重写ModelAdmin的方法 """
    # # 当前后台登录用户自动保存为作者
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # 只显示作者为当前用户的文章
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)
    # --------------------------------- #

    """ 引入自定义静态资源 """
    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css', ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js', )


# 日志
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
