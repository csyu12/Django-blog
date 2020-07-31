import mistune
from django import forms

from .models import Comment


# 前端评论渲染
class CommentForm(forms.ModelForm):
    # 重新定义需要在前端展示的字段，可以随时修改样式
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )
    email = forms.CharField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'rows': 6, 'cols': 50, 'class': 'form-control'}
        )
    )

    # clean_xxx：处理对应字段数据的方法
    def clean_content(self):
        content = self.cleaned_data.get('content')
        # 控制评论的长度，如果内容太少，直接抛出异常
        if len(content) < 10:
            raise forms.ValidationError('短了！！！')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']
