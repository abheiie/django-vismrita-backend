from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('posts/bookmarked/', views.BookmarkedPostList.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('likes/', views.LikeDetail.as_view()),
    path('bookmarks/', views.BookmarkDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)