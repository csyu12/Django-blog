from django.urls import path, re_path
from . import views
from .views import CommentView

urlpatterns = [
    path('', CommentView.as_view(), name='index'),
]
