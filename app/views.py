from django.shortcuts import render
from django.http import StreamingHttpResponse
from .models import Post, PostType, Article, FilePost
from .forms import MyForm
import os, time
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
    if request.method == 'POST' and request.user.is_authenticated:
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
    # show all the post ordered by date, handling is defined in template
    result = Post.objects.select_related('article', 'filepost').order_by('-date_created')

    return render(request, 'app/index.html', {'form': form, 'result': result, 'message': message})



def stream(file):
    file = file.replace('/media/','')
    base = settings.BASE_DIR
    path = os.path.join(settings.MEDIA_ROOT,file)

    with open(path,'rb') as open_file:
        yield open_file.read()

# function to handle filestreams of images and videos
def vid(request, filepost):
    return StreamingHttpResponse(stream(filepost))

