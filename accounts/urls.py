from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('update-follow/<int:following_id>/', views.ContactDetail.as_view()),
    path('followers/', views.FollowerList.as_view()),
    path('followings/', views.FollowingList.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    # path('users/me/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)