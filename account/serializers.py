from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile

# User serializer
class UserSerializer(serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = ("id","username","email",)

#Register serializer
class RegisterSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password":{"write_only":True}}

    def create(self, validated_data)  :
        user = User.objects.create_user(validated_data["username"], validated_data["email"],validated_data["password"])
        UserProfile.objects.create(user=user)
        return user
        

# Login serializer

class LoginSerializer(serializers.Serializer) :
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data) :
        user = authenticate(**data)

        if user and user.is_active :
            return user
        raise serializers.ValidationError("incorrect credentials")
    

# update UserProfile serializer

class UserProfileSerializer(serializers.ModelSerializer) :
    class Meta :
        model = UserProfile
        fields = "__all__"

    def update(self, instance, validated_data) :
        profile = UserProfile.objects.update(**validated_data)
        return profile


# class UpdateUserProfileSerializer(serializers.ModelSerializer) :
#     def update(self, instance, validated_data) :
#         instance.image = validated_data["image"]
#         instance.description = validated_data["description"]
#         instance.save()
#         user = self.context["user"]
#         profile = UserProfile.objects.update(user,**validated_data)
#         profile.save()
#         return profile


