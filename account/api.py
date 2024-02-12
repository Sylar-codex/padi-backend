from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth.models import User
from knox.auth import TokenAuthentication
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, UserProfileSerializer
from rest_framework.decorators import action
from .models import UserProfile

# register api
class RegisterAPI(generics.GenericAPIView) :
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs) :
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response ({
            "user": UserSerializer(user, context = self.get_serializer()).data,
            "token": AuthToken.objects.create(user)[1]
        })
    
# login api 
class LoginAPI(generics.GenericAPIView) :
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwags) :
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response ({
            "user": UserSerializer(user, context = self.get_serializer()).data,
            "token":AuthToken.objects.create(user)[1]
        })
    
# user api
class UserAPI(generics.RetrieveAPIView) :
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user


    
# get all users
class AllUsersAPI(generics.RetrieveAPIView) :
    serializer_class = UserSerializer

    authentication_classes = (TokenAuthentication,)

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    def get(self, request) :
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True, context={"request":request})

        return Response(serializer.data)
    


class UpdateUserProfileAPI(generics.UpdateAPIView) :
    serializer_class = UserProfileSerializer

    authentication_classes = (TokenAuthentication,)

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = UserProfile.objects.all()

    
    def patch(self, request,*args,**kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"user profile updated"})




class GetUserProfileAPI(generics.RetrieveAPIView) :
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user.user_profile

