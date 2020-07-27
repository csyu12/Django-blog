from django import forms


# 定义后台管理form，增加更多自定义字段功能
class PostAdminForm(forms.ModelForm):
    # textarea多行多列
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)

