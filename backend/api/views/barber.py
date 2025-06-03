from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from ..utils import (
    IsBarberRole,
)
from ..serializers import (
    AddServiceSerializer,
)


@api_view(['POST'])
@permission_classes([IsBarberRole])
def add_service(request):
    """
    Barber only: Adds a new service to the authenticated Barber
    """
    serializer = AddServiceSerializer(data=request.data, context={'barber_id': request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Service added successfully.'}, status=status.HTTP_201_CREATED)
