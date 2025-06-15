from rest_framework import serializers
from ..utils import(
    GetBarbersMixin,
)


class GetBarberListSerializer(GetBarbersMixin, serializers.Serializer):
    """
    Return a list of all active barbers
    """
    def to_representation(self, instance):
        barbers = self.get_barbers_public()
        return {'barbers': barbers}
    