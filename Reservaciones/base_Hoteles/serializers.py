from rest_framework import serializers
from .models import User, Room, Reservation, Stay

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = '__all__'
