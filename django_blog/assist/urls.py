from django.urls import path

from .views import LinkListView

urlpatterns = [
    path('links/', LinkListView.as_view(), name='links'),
]
