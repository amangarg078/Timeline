from django import forms


class MyForm(forms.Form):
    description = forms.CharField()
    article_text = forms.CharField(widget=forms.Textarea, required=False)
    upload = forms.FileField(required=False)


