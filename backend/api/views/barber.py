from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from ..utils import (
    IsBarberRole,
)
from ..serializers import (
    AddServiceSerializer,
    UpdateServiceSerializer,
    DeleteServiceSerializer
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


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsBarberRole])
def manage_service(request, service_id):
    """
    Barber only: Manages a service with (UPDATE, DELETE operations).
    """
    
    if request.method == 'PATCH':
        serializer = UpdateServiceSerializer(data=request.data, context={'service_id': service_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({'detail': 'Service edited successfully.'}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        serializer = DeleteServiceSerializer(data={"id": service_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()

    return Response({"detail": f"Service with ID {service_id} has been deleted."}, status=status.HTTP_200_OK)
    