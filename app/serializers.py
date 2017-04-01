from rest_framework import serializers
from .models import Article, FilePost, Post

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ( 'id','username', 'description', 'article_text', 'date_created')

    def get_username(self, obj):
        return obj.user.username

class FilePostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = FilePost
        fields = ('id', 'username', 'post_type_id', 'description', 'file', 'date_created')
    def get_post_type_id(self):
        return self.context["post_type_id"]
    def get_username(self, obj):
        return obj.user.username

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'post_type','username', 'description', 'content', 'date_created')

    def get_content(self, obj):
        if obj.post_type_id == 1:
            return "Article"
        elif obj.post_type_id == 2:
            return "Image"
        elif obj.post_type_id == 3:
            return "Video"

    def get_username(self, obj):
        return obj.user.username

