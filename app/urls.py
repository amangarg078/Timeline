from django.conf.urls import url
from rest_framework.authtoken import views as rest_framework_views

from . import views

urlpatterns = [
    url(r'^api-auth-token/', rest_framework_views.obtain_auth_token),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^vid/(.?media.+)', views.vid, name='vid'),
    url(r'^post/(?P<id>[0-9]+)/$',views.PostDetails.as_view(), name='post_details'),
    url(r'^v1/post/$', views.PostListAPIView.as_view(), name='post_list'),
    url(r'^v1/post/article/$', views.ArticleListAPIView.as_view(), name='article_list'),
    url(r'^v1/post/file/$', views.FileListAPIView.as_view(), name='file_list'),
    url(r'^v1/post/article/upload/$', views.ArticleUploadAPIView.as_view(), name='article_upload'),
    url(r'^v1/post/file/upload/$', views.FileUploadAPIView.as_view(), name='file_upload'),
    url(r'^v1/post/article/(?P<pk>[0-9]+)$', views.ArticleGetEditDeleteAPIView.as_view(), name='article_get_put_delete'),
    url(r'^v1/post/file/(?P<pk>[0-9]+)$', views.FilePostGetEditDeleteAPIView.as_view(), name='file_get_put_delete'),
    ]