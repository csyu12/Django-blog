from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


""" sitemap（站点地图）描述网站的内容组织结构，提供给搜索引擎，更好收录本网站 """


class PostSitemap(Sitemap):
    changefreq = 'always'
    priority = 1.0
    protocol = 'https'

    def items(self):    # 返回所有正常状态的文章
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self, obj):     # 返回每篇文章的创建世界
        return obj.created_time

    def location(self, obj):    # 返回每篇文章的URL
        return reverse('blog:post_detail', args=[obj.pk])
