from rest_framework import serializers
from ..utils import(
    UserValidationMixin,
)

class UploadProfileImageSerializer(UserValidationMixin, serializers.Serializer):
    """
    Uploads a profile image to the profile of a given user
    """
    profile_image = serializers.ImageField(required=True)

    def validate(self, attrs):
        attrs = self.validate_user(attrs)
        return attrs

    def update(self, instance, validated_data):
        instance.profile_image.delete(save=False) # Delete previous image (if any) before updating
        instance.profile_image = validated_data['profile_image']
        instance.save()
        return instance
    
    def save(self, **kwargs):
        return self.update(self.validated_data['user'], self.validated_data)


class DeleteProfileImageSerializer(UserValidationMixin, serializers.Serializer):
    """
    Deletes the profile picture for a given user
    """
    def validate(self, attrs):
        attrs = self.validate_user(attrs)
        return attrs

    def delete(self):
        user = self.validated_data['user']
        user.profile_image.delete(save=False)
        user.profile_image = None
        user.save()