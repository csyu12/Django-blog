import mistune
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from django.db import models


"""博客内容相关模型"""


# 博客分类
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=40, verbose_name='分类名称')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    # 获取所有分类，并区分导航和普通分类
    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:     # 只进行了一次I/O操作
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


# 博客标签
class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name='标签名称')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


# 博客主体
class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=128, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    content_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1)     # 网页点击量，用户对同一页面多次访问，pv累计
    uv = models.PositiveIntegerField(default=1)     # 浏览网页的自然人，本项目中用uuid指定唯一用户，1天内重复访问同一页面，uv不累计

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save(*args, **kwargs)

    @staticmethod   # 声明静态方法，获取标签id指定博客
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')

        return post_list, tag

    @staticmethod   # 声明静态方法，获取分类id指定博客
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoedNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')

        return post_list, category

    @classmethod    # 获取最新文章
    def latest_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    @classmethod    # 获取热门文章
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    # 把返回的数据绑到实例上，不用每次访问时都去执行tags函数中的代码
    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))
