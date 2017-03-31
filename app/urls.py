from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^vid/(.?media.+)', views.vid, name='vid'),
    url(r'^post/(?P<id>[0-9]+)/$',views.postDetails, name='post_details')
    ]