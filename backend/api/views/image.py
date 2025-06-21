from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from ..serializers import (
    UploadProfileImageSerializer,
    DeleteProfileImageSerializer,
)


@extend_schema(
    methods=['POST'],
    request=UploadProfileImageSerializer,
    # request=OpenApiTypes.BINARY,
    responses={200: OpenApiResponse(description="Profile picture uploaded successfully.")},
    description="Uploads a profile image to the profile of the authenticated user.",
)
@extend_schema(
    methods=['DELETE'],
    responses={204: OpenApiResponse(description="Profile picture deleted successfully.")},
    description="Deletes the profile picture of the authenticated user.",
)
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([FileUploadParser])
def manage_profile_picture(request):
    """
    Handles update and delete operations for the profile image of the authenticated user.

    - POST: Uploads a profile image to the profile of the authenticated user.
    - DELETE: Deletes the profile picture of the authenticated user.
    """
    if request.method == 'POST':
        serializer = UploadProfileImageSerializer(data=request.data, context={'user_id': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"detail": "Profile picture uploaded successfully."}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        serializer = DeleteProfileImageSerializer(data={}, context={'user_id': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
