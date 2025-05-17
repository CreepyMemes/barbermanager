from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..serializers import (
    GetUserSerializer,
)


User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """
    Return the authenticated user's information.
    """
    serializer = GetUserSerializer(request.user)
    return Response(serializer.data)