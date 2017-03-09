from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class PostType(models.Model):
    type = models.CharField(max_length=128)

    def __unicode__(self):
        return self.type


class Post(models.Model):
    post_type = models.ForeignKey(PostType)
    user = models.ForeignKey(User)
    description = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{0} - {1}'.format(self.user, self.post_type)


class Article(Post):
    article_text = models.TextField()

    def __unicode__(self):
        return self.post_type.type


class FilePost(Post):
    file = models.FileField(upload_to=user_directory_path)

    def __unicode__(self):
        return self.post_type.type
