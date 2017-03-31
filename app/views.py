from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse
from .models import Post, PostType, Article, FilePost
from .forms import MyForm
import os
from django.core.cache import cache
from django.conf import settings

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


def index(request):
    form = MyForm()
    message = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MyForm(request.POST, request.FILES)
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
                if cache.get(request.user.id):
                    cache.delete(request.user.id)
    # show all the post ordered by date, handling is defined in template
        result = cache.get(request.user.id)

        if not result:
            query_result = Post.objects.select_related('article', 'filepost').order_by('-date_created')
            cache.set(request.user.id, query_result, 60)
            result = cache.get(request.user.id)

    else:
        result = cache.get("Anonymous")

        if not result:
            query_result = Post.objects.select_related('article', 'filepost').order_by('-date_created')
            cache.set("Anonymous", query_result, 60)
            result = cache.get("Anonymous")

    return render(request, 'app/index.html', {'form': form, 'result': result, 'message': message})



def stream(file):
    file = file.replace('/media/','')
    base = settings.BASE_DIR
    path = os.path.join(settings.MEDIA_ROOT,file)
    print path
    print settings.MEDIA_ROOT

    with open(path,'rb') as open_file:
        yield open_file.read()

# function to handle filestreams of images and videos
def vid(request, filepost):
    return StreamingHttpResponse(stream(filepost))



def postDetails(request,id):

    if request.user.is_authenticated:
        result = cache.get(str(request.user.id)+'a'+str(id))
        if not result:
            post = get_object_or_404(Post.objects.select_related('article','filepost'), pk=id)
            cache.set(str(request.user.id)+'a'+str(id), post, 60)
            result = cache.get(str(request.user.id)+'a'+str(id))

    else:
        result = cache.get("Anonymous"+'a'+str(id))
        if not result:
            post = get_object_or_404(Post.objects.select_related('article','filepost'), pk=id)
            cache.set("Anonymous"+'a'+str(id), post, 60)
            result = cache.get("Anonymous"+'a'+str(id))
    return render(request, 'app/details.html', {'result':result})





