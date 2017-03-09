from django import forms

from .models import Article, Post, FilePost

class MyForm(forms.Form):
    description = forms.CharField()
    article_text = forms.CharField(widget=forms.Textarea,required=False)
    upload=forms.FileField(required=False)





class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=['article_text',]

class FileForm(forms.ModelForm):
    class Meta:
        model=FilePost
        fields=['file',]
