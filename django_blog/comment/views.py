from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm


# 处理评论内容
class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'   # 结果渲染页

    def post(self, request, *args, **kwargs):
        # 交由 CommentForm 接收并处理数据
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        # 验证保存表单数据
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target,
        }
        return self.render_to_response(context)

