from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (
    GetBarberListSerializer,
)
from ..models import (
    Barber, 
    Availability
)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def get_barbers_list(request):
    """
    Return a list of all active barbers
    """
    barbers = Barber.objects.filter(is_active=True)
    serializer = GetBarberListSerializer(barbers, many=True)
    return Response({"barbers": serializer.data}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
def get_barber_public_availability(request, barber_id):
    availabilities = Availability.objects.filter(barber_id=barber_id)
    data = [
        {
            "date": a.date,
            "slots": a.slots
        }
        for a in availabilities
    ]
    return Response({"availability": data}, status=200)