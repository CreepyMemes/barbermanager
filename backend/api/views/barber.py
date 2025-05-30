from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..serializers import (
    AddServiceSerializer,
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_service(request):
    """
    Barber-only: aggiunge un nuovo servizio.
    """
    serializer = AddServiceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    service = serializer.save()

    return Response({'detail': 'Service added'}, status=status.HTTP_201_CREATED)
