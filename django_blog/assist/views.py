from django.shortcuts import render, HttpResponse
from django.views.generic import ListView

from blog.views import CommonViewMixin
from .models import Link


class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'assist/links.html'
    context_object_name = 'link_list'



