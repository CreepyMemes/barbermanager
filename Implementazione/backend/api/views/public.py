from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models import Barber
from ..serializers import (
    GetBarberListSerializer,
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