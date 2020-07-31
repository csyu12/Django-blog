from django import forms


class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='评论内容')
