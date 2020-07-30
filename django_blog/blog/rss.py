from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post


""" RSS（简易信息聚合）用来提供订阅接口，用户可通过RSS阅读器订阅我们的网站 """


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    feed_type = Rss201rev2Feed  # 默认Rss201rev2Feed，可改
    title = 'Multi-person Blog System'
    link = '/rss/'
    description = 'Multi-person is a blog system power by django'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.pk])

    def item_description(self, item):
        return item.desc

    def item_extra_kwargs(self, item):
        return {'content_html': self.item_content_html(item)}

    def item_content_html(self, item):
        return item.content_html
