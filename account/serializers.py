from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile
from cloudinary.uploader import upload_image
import os

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
    remove_image = serializers.BooleanField(default=False)
    class Meta :
        model = UserProfile
        fields = "__all__"
    def update(self, instance, validated_data) :
        user = self.context["request"].user
        if "remove_image" in validated_data :
            if validated_data["remove_image"] :
                return UserProfile.objects.filter(user=user).update(image=None)

        if "image" in validated_data :
            validated_data["image"] = upload_image(validated_data["image"], use_filename=True, folder="profile_image/", api_key=os.environ.get("CLOUDINARY_API_KEY"))

            
        profile = UserProfile.objects.filter(user=user).update(**validated_data)
        return profile




