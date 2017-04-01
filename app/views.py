from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse
from .models import Post, PostType, Article, FilePost
from .forms import MyForm
import os
from django.core.cache import cache
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import generics
from .serializers import ArticleSerializer, FilePostSerializer, PostSerializer
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication


def filehandler(request, upload):
    ext = os.path.splitext(upload.name)[1]
    image_list = ['.jpg', '.jpeg', '.png']
    video_list = ['mp4', 'wmv', 'mkv', 'avi', 'mov']
    if ext in image_list:
        p = PostType.objects.values().filter(type="Image")[0]
        return p['id']
    elif ext in video_list:
        p = PostType.objects.values().filter(type="Video")[0]
        return p['id']
    return None


def cache_handler(request, key, value):
    CACHE_TTL = settings.CACHE_TTL
    if request.user.is_authenticated:
        key = str(request.user.id) + key
        result = cache.get(key)
        if not result:
            cache.set(key, value, CACHE_TTL)
            result = cache.get(key)

    else:
        key = "Anonymous" + key
        result = cache.get(key)
        if not result:
            cache.set(key, value, CACHE_TTL)
            result = cache.get(key)
    return result


def form_handler(request, form):
    if form.is_valid():
        article_text = form.cleaned_data['article_text']
        description = form.cleaned_data['description']
        if 'upload' in request.FILES:
            upload = request.FILES['upload']
        else:
            upload = None
        # check if the post is an article
        if (upload is None) and article_text:
            article = Article.objects.create(post_type_id=1, article_text=article_text, description=description,
                                             user=request.user)
            form = MyForm()

            # check if the post is a file upload and handle the upload
        elif (upload is not None) and (not article_text):
            post_type_id = filehandler(request, upload)
            if post_type_id is not None:
                filepost = FilePost.objects.create(post_type_id=post_type_id, user=request.user, file=upload,
                                                   description=description)
            else:
                message = "Invalid File"
            form = MyForm()
        else:
            message = "Enter either an article or a file"

        return form
    else:
        form = MyForm()
        return form






class IndexView(TemplateView):
    form_class = MyForm
    template_name = 'app/index.html'
    key = ''
    value = Post.objects.select_related('article', 'filepost').order_by('-date_created')

    def get(self, request, *args, **kwargs):
        result = cache_handler(request, self.key, self.value)
        form = MyForm()
        form = form_handler(request, form)
        return render(request, self.template_name, {'form': form, 'result': result})

    def post(self, request, *args, **kwargs):
        result = cache_handler(request, self.key, self.value)
        form = self.form_class(request.POST, request.FILES)
        form = form_handler(request, form)
        if cache.get(request.user.id):
            cache.delete(request.user.id)

        return render(request, self.template_name, {'form': form, 'result': result})


def stream(file):
    file = file.replace('/media/', '')
    base = settings.BASE_DIR
    path = os.path.join(settings.MEDIA_ROOT, file)
    print path
    print settings.MEDIA_ROOT

    with open(path, 'rb') as open_file:
        yield open_file.read()


# function to handle filestreams of images and videos
def vid(request, filepost):
    return StreamingHttpResponse(stream(filepost))


class PostDetails(TemplateView):
    model = Post
    template_name = 'app/details.html'
    def render_to_response(self, context, *args, **kwargs):
        request = self.request
        id = self.kwargs['id']
        key = 'a' + str(id)
        value = get_object_or_404(Post.objects.select_related('article', 'filepost'), pk=id)
        result = cache_handler(request, key, value)
        return render(request,self.template_name , {'result': result})



class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('article', 'filepost').order_by('-date_created')

@authentication_classes(TokenAuthentication)
class ArticleAPIView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

@authentication_classes(TokenAuthentication)
class FileUploadAPIView(generics.CreateAPIView):
    serializer_class = FilePostSerializer
    queryset = FilePost.objects.all()







