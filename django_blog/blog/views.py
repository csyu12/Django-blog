from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Tag, Category
from assist.models import SideBar
from comment.forms import CommentForm, Comment


""" class-based view """
# 首页
class IndexView(ListView):
    queryset = Post.latest_posts()  # 最新帖子
    paginate_by = 5     # 分页
    context_object_name = 'post_list'   # 如果不设置此项，在模板中需要使用object_list变量
    template_name = 'blog/list.html'    # 指定模板


# 分类
class CategoryView(IndexView):
    """
    处理流程：
    1. 调用get_queryset拿到数据源
    2. 调用get_context_data拿到需要渲染到模板中的数据
    3. 调用render_to_response渲染数据到页面
    """
    def get_context_data(self, *, object_list=None, **kwargs):
        """ 重写get_context_data，获取上下文数据，并更新context """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)  # 根据分类ID获取实例对象，不存在抛出404
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """ 重写queryset，根据分类ID过滤 """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


# 标签
class TagView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)     # 根据标签ID获取实例对象，不存在抛出404
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写queryset，根据标签ID过滤 """
        # queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        tag_obj = Tag.objects.get(id=tag_id)
        return tag_obj.post_set.filter(status=Post.STATUS_NORMAL)   # 反向获取post对象
        # return queryset.filter(tag_id=tag_id) # tag是多对多关系，queryset里没有tag_id


# 通用数据模板，如：分类导航、侧边栏、底部导航等
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


# 详情页
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_target(self.request.path),
        })
        return context


# 搜索
class SearchView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


""" function view """
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         post_s, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_s, category = Post.get_by_category(category_id)
#     else:
#         post_s = Post.latest_posts()
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_s,
#         'sidebars': SideBar.get_all()
#     }
#     context.update(Category.get_navs())     # 添加分类数据
#     return render(request, 'blog/list.html', context=context)
#
#
# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all()
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)
