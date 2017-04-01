from django.conf.urls import url
from rest_framework.authtoken import views as rest_framework_views

from . import views

urlpatterns = [
    url(r'^api-auth-token/', rest_framework_views.obtain_auth_token),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^vid/(.?media.+)', views.vid, name='vid'),
    url(r'^post/(?P<id>[0-9]+)/$',views.PostDetails.as_view(), name='post_details'),
    url(r'^v1/post/$', views.PostListAPIView.as_view(), name='post_list'),
    #url(r'^v1/post/(?P<pk>[0-9]+)$', views.reimbursement_detail, name='reimbursement_detail'),

    ]