from django.urls import path, re_path

# from . import views
from .views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView
)

urlpatterns = [
    # path('', views.post_list, name='index'),
    # path('category/<int:category_id>/', views.post_list, name='category_list'),
    # path('tag/<int:tag_id>/', views.post_list, name='tag_list'),
    # path('post/<int:post_id>', views.post_detail, name='post_detail'),

    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category_list'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag_list'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchView.as_view(), name='search'),
]
