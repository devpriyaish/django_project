from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = ['content', 'date_posted', 'author']


def create(self, validate_data):
    return Post.objects.create(**validate_data)