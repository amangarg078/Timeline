from django.contrib import admin

# Register your models here.
from .models import Post, PostType, Article, FilePost


admin.site.register(PostType)
admin.site.register(Post)

admin.site.register(Article)
admin.site.register(FilePost)
