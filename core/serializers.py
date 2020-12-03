from rest_framework import serializers
from .models import Post, Bookmark, Comment


class PostSerializer(serializers.ModelSerializer):

    owner_id = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    owner_first_name = serializers.ReadOnlyField(source='owner.first_name')
    owner_last_name = serializers.ReadOnlyField(source='owner.last_name')

    class Meta:
        model = Post
        fields = ('id', 'category', 'content', 'created_at',  'updated_at', 'owner_id', 'owner_username', 'owner_first_name', 'owner_last_name')



class BookmarkSerializer(serializers.ModelSerializer):

    post_id = serializers.ReadOnlyField(source='post.id')
    post_owner_id = serializers.ReadOnlyField(source='post.owner.id')
    post_owner_username = serializers.ReadOnlyField(source='post.owner.username')
    post_owner_first_name = serializers.ReadOnlyField(source='post.owner.first_name')
    post_owner_last_name = serializers.ReadOnlyField(source='post.owner.last_name')
    post_content = serializers.ReadOnlyField(source='post.content')

    class Meta:
        model = Bookmark
        fields = (
            'id',
            'owner', 
            'post_id', 
            'post_owner_id', 
            'post_content', 
            'post_owner_first_name', 
            'post_owner_last_name', 
            'post_owner_username')


class CommentSerializer(serializers.ModelSerializer):

    # post_id = serializers.ReadOnlyField(source='post.id')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    owner_first_name = serializers.ReadOnlyField(source='owner.first_name')
    owner_last_name = serializers.ReadOnlyField(source='owner.last_name')

    class Meta:
        model = Comment
        fields = (
            'id', 
            'content', 
            'created_at', 
            'updated_at', 
            'post', 
            'owner_id', 
            'owner_username',
            'owner_first_name', 
            'owner_last_name', 
            )

class LikeSerializer(serializers.ModelSerializer):

    post = serializers.ReadOnlyField(source='post.id')
    post_owner_id = serializers.ReadOnlyField(source='post.owner.id')
    post_owner_username = serializers.ReadOnlyField(source='post.owner.username')
    post_owner_first_name = serializers.ReadOnlyField(source='post.owner.first_name')
    post_owner_last_name = serializers.ReadOnlyField(source='post.owner.last_name')
    post_content = serializers.ReadOnlyField(source='post.content')

    class Meta:
        model = Bookmark
        fields = (
            'id',
            'owner', 
            'post', 
            'post_owner_id', 
            'post_content', 
            'post_owner_first_name', 
            'post_owner_last_name', 
            'post_owner_username')


