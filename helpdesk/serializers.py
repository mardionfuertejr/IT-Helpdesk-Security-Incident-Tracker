from rest_framework import serializers
from .models import Ticket, CustomUser, TicketUpdate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'role', 'department', 'profile_picture', 'created_at']

class TicketUpdateSerializer(serializers.ModelSerializer):
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = TicketUpdate
        fields = ['id', 'comment', 'updated_by', 'created_at']

class LegacyTicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updates = TicketUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'created_by', 'title', 'category', 'priority',
            'description', 'attachment', 'status', 'created_at', 'updated_at',
            'updates'
        ]

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'ticket_type', 'nist_stage', 'priority',
            'is_resolved', 'created_at'
        ]
