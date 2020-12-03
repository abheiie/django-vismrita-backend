from .models import User, Contact
from .serializers import UserSerializer, ContactSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination


class FollowerList(APIView, LimitOffsetPagination):
    ''' 
    get the follower of user whome user_id is passed here, 
    '''
    def get(self, request, format=None):

        data = {}
        user_id = request.GET.get('user_id')

        followers = Contact.objects.filter(following_id = user_id )
        results = self.paginate_queryset(followers, request, view=self)
        serializer = ContactSerializer(results, many=True)
        response = serializer.data

        for follower in response:
            print("---->", follower)
            following_id = follower['owner']

            print("following_id====>", following_id)

            check = None
            #to check if current user is following this user or not
            try:
                check = Contact.objects.get(owner = request.user, following_id = following_id)
            except:
                check = None
            
            is_following  = False
            if check is not None:
                is_following = True
            follower["is_following"] = is_following

        return Response(response)

class FollowingList(APIView, LimitOffsetPagination):
    ''' 
    get the list of user whome user follows
    '''
    def get(self, request, format=None):

        data = {}
        user_id = request.GET.get('user_id')

        followings = Contact.objects.filter(owner_id = user_id )
        results = self.paginate_queryset(followings, request, view=self)
        serializer = ContactSerializer(results, many=True)
        response = serializer.data

        for following in response:
            print("---->", following)
            follower_id = following['following']

            print("follower_id====>", follower_id)

            check = None
            #to check if current user is following this user or not
            try:
                check = Contact.objects.get(owner = request.user, following_id = follower_id)
            except:
                check = None
            
            is_following  = False
            if check is not None:
                is_following = True
            following["is_following"] = is_following

        return Response(response)

class ContactDetail(APIView):
    '''
    Follow or unfollow a user
    '''
    def post(self, request, following_id, format=None):
        
        try:
            contact = Contact.objects.get(owner=request.user, following_id=following_id)
        except:
            contact = None

        if contact is not None:
            '''
            if user is already following
            '''
            if contact.owner == request.user:
                contact.delete()
                following = User.objects.get(id = following_id)
                serializer = UserSerializer(following)
                response = serializer.data
                response["is_following"] = False
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(unauthorised_statement, status=status.HTTP_401_UNAUTHORIZED)
        else:
            '''
            if user is not following
            '''
            contact = Contact(owner=request.user, following_id=following_id)
            contact.save()
            following = User.objects.get(id = following_id)
            serializer = UserSerializer(following)
            response = serializer.data
            response["is_following"] = True
            return Response(response)

class UserList(APIView, LimitOffsetPagination):
    ''' 
    get the list of user whome user follows
    '''
    def get(self, request, format=None):

        users = User.objects.all().exclude(id = request.user.id)
        results = self.paginate_queryset(users, request, view=self)
        serializer = UserSerializer(results, many=True)
        response = serializer.data

        for user in response:
            check = None
            try:
                check = Contact.objects.get(owner = request.user, following_id = user['id'])
            except:
                check = None

            is_following  = False
            if check is not None:
                is_following = True
            user["is_following"] = is_following

        return Response(response)

class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("you are not authorised", status=status.HTTP_401_UNAUTHORIZED)



    #TODO this has to be done in future
    # def delete(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     snippet.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
















# #TODO
# 1) api for all users
# 2) api for signup
# 3) api for login
# 4) api for profile 
# 5) api for edit profile




# class EditProfile(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     def get(self, request, format=None):
#         couser = Couser.objects.get(id = request.id)
#         serializer = CouserSerializer(couser)
#         return Response(serializer.data)











