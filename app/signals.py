from .models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
'''
@receiver(post_save, sender=Post)
def index_post(sender, instance, **kwargs):
    instance.indexing()
'''

@receiver(post_save, sender = Post)
def clear_cache(sender, **kwargs):
    cache.clear()