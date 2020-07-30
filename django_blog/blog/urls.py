from django.urls import path, re_path
from django.contrib.sitemaps import views as sitemap_views

from .views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView, AuthorView
)
from .rss import LatestPostFeed
from .sitemap import PostSitemap


urlpatterns = [
    # function view
    # path('', views.post_list, name='index'),
    # path('category/<int:category_id>/', views.post_list, name='category_list'),
    # path('tag/<int:tag_id>/', views.post_list, name='tag_list'),
    # path('post/<int:post_id>', views.post_detail, name='post_detail'),

    # class-based view
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category_list'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag_list'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('author/<int:owner_id>/', AuthorView.as_view(), name='author'),
    re_path('rss|feed/', LatestPostFeed(), name='rss'),
    re_path('sitemap\.xml', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
]
