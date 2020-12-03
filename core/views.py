from .models import Post, Like, Bookmark, Comment
from .serializers import PostSerializer, BookmarkSerializer, CommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework import generics
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination

unauthorised_statement = "You are Unauthorised"

class PostList(APIView, LimitOffsetPagination):
    """
    List all posts, or create a new post. 
    """
    def get(self, request, format=None):
        """ 
        Any user can access this view 
        """
        posts = Post.objects.all()
        results = self.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(results, many=True)

        # if current user liked or bookmarked this post or not
        liked = False
        bookmarked = False
        for post in serializer.data:
            post_obj = Post.objects.get(id = post["id"])
            try:
                like_object = Like.objects.filter(owner = request.user, post = post_obj)
                if like_object.count() > 0:
                    post["liked"] = True
                else:
                    post["liked"] = False

                bookmark_object = Bookmark.objects.filter(owner = request.user, post = post_obj)
                if bookmark_object.count() > 0:
                    post["bookmarked"] = True
                else:
                    post["bookmarked"] = False

                post["likes_count"] = post_obj.likes.count()
                post["comments_count"] = post_obj.comments.count()
                post["bookmarks_count"] = post_obj.bookmarks.count()
            except:
                pass
        return Response(serializer.data)


    def post(self, request, format=None):
        """ 
        Any user can access this view 
        """
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookmarkedPostList(APIView, LimitOffsetPagination):
    """
    List all bookmarked posts by owner
    """
    def get(self, request, format=None):
        """ 
        owner can can access this view 
        """
        bookmarks = request.user.bookmarks.all()
        results = self.paginate_queryset(bookmarks, request, view=self)
        serializer = BookmarkSerializer(results, many=True)
        return Response(serializer.data)

class PostDetail(APIView):
    """
    Retrieve, update or delete a post instance.
    """

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ 
        Any user can access this view 
        """
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        response = serializer.data

        like_object = Like.objects.filter(owner = request.user, post = post)
        if like_object.count() > 0:
            response["liked"] = True
        else:
            response["liked"] = False

        bookmark_object = Bookmark.objects.filter(owner = request.user, post = post)
        if bookmark_object.count() > 0:
            response["bookmarked"] = True
        else:
            response["bookmarked"] = False
        
        response["likes_count"] = post.likes.count()
        response["comments_count"] = post.comments.count()
        response["bookmarks_count"] = post.bookmarks.count()

        return Response(response)

    def put(self, request, pk, format=None):
        """ 
        only owner can access this view 
        """
        post = self.get_object(pk)

        if post.owner == request.user:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(unauthorised_statement, status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, pk, format=None):
        """ 
        only owner can access this view 
        """
        post = self.get_object(pk)
        if post.owner == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(unauthorised_statement, status=status.HTTP_401_UNAUTHORIZED)



class CommentList(APIView, LimitOffsetPagination):
    """
    List of all comments of particular post, or create a new comment on a post. 
    """

    def get(self, request, format=None):
        """ 
        user can access this view 
        """
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id = post_id)
        comments = post.comments.all()
        results = self.paginate_queryset(comments, request, view=self)
        serializer = CommentSerializer(results, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        """ 
        user can access this view 
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommentDetail(APIView):
    """
    Retrieve, update or delete a comment on a post.
    """

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ 
        Any user can access this view, get comment of a post
        """
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        response = serializer.data
        return Response(response)

    def put(self, request, pk, format=None):
        """ 
        only owner can access this view, edit the comment
        """
        comment = self.get_object(pk)

        if comment.owner == request.user:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(unauthorised_statement, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        """ 
        only owner can access this view, delete the comment
        """
        comment = self.get_object(pk)
        if comment.owner == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(unauthorised_statement, status=status.HTTP_401_UNAUTHORIZED)


class LikeDetail(APIView):
    """
    like or dislike a post, will return a post instance 
    """
    def post(self, request, format=None):

        data = {}
        post_id = request.GET.get('post_id')

        try:
            like = Like.objects.get(post_id=post_id, owner=request.user)
        except:
            like = None

        if like is not None:
            '''
            if post is not already liked
            '''
            if like.owner == request.user:
                like.delete()
                post = Post.objects.get(id=post_id)
                data["id"] = post.id
                data["liked"] = False
                data["likes_count"] = post.likes.count()
                return Response(data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(unauthorised_statement, status=status.HTTP_401_UNAUTHORIZED)

        else:
            '''
            if post is not already liked
            '''
            post = Post.objects.get(id=post_id)
            like = Like(owner=request.user, post=post)
            like.save()
            data["id"] = post.id
            data["liked"] = True
            data["likes_count"] = post.likes.count()
            return Response(data, status=status.HTTP_201_CREATED)
        

class BookmarkDetail(APIView):
    """
    bookmark or unbookmark a post, will return a post instance 
    """

    def post(self, request, format=None):

        data = {}
        post_id = request.GET.get('post_id')

        try:
            bookmark = Bookmark.objects.get(post_id=post_id, owner=request.user)
        except:
            bookmark = None

        if bookmark is not None:
            '''
            if post is already bookmarked
            '''
            if bookmark.owner == request.user:
                bookmark.delete()
                post = Post.objects.get(id=post_id)
                data["id"] = post.id
                data["bookmarked"] = False
                data["bookmarks_count"] = post.bookmarks.count()
                return Response(data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(unauthorised_statement, status=status.HTTP_401_UNAUTHORIZED)

        else:
            '''
            if post is not already bookmarked
            '''
            post = Post.objects.get(id=post_id)
            bookmark = Bookmark(owner=request.user, post=post)
            bookmark.save()
            data["id"] = post.id
            data["bookmarked"] = True
            data["bookmarks_count"] = post.bookmarks.count()
            return Response(data, status=status.HTTP_201_CREATED)
