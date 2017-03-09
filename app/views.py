from django.shortcuts import render, get_object_or_404
from .models import Post, PostType, Article, FilePost, User
from .forms import MyForm
from django.http import HttpResponseRedirect
import re
from datetime import datetime
from django.core.urlresolvers import reverse
# Create your views here.

def filehandler(request, description, upload):
    import os

    ext = os.path.splitext(upload.name)[1]
    print ext
    image_list = ['.jpg', '.jpeg', '.png']
    video_list = ['mp4', 'wmv', 'mkv', 'avi', 'mov']
    if ext in image_list:
        p = PostType.objects.values().filter(type="Image")[0]
        return p['id']
    elif ext in video_list:
        p = PostType.objects.values().filter(type="Video")[0]
        return p['id']
    return None


def index(request):
    form = MyForm()
    message = None
    if request.method == 'POST' and request.user.is_authenticated:
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            upload = request.FILES['upload']
            article_text = form.cleaned_data['article_text']
            description = form.cleaned_data['description']

            if (upload is None) and article_text:
                article = Article.objects.create(post_type_id=1, article_text=article_text, description=description,
                                                 user=request.user)
                form = MyForm()

            elif (upload is not None) and (not article_text):
                post_type_id = filehandler(request, description, upload)
                if post_type_id is not None:
                    filepost = FilePost(post_type_id=post_type_id, user=request.user, file=upload,
                                        description=description)
                else:
                    message = "invalid File"
                form = MyForm()
            else:
                message = "Enter only one"
    result = Post.objects.select_related('article', 'filepost').order_by('-date_created')

    return render(request, 'app/index.html', {'form': form, 'result': result, 'message': message})

