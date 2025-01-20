from rest_framework import serializers
from .models import ServiceRequest

class ServiceRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving service requests, including file attachments.
    """
    class Meta:
        model = ServiceRequest
        fields = ['id', 'request_type', 'details', 'file', 'status', 'submitted_at', 'resolved_at']
        read_only_fields = ['id', 'status', 'submitted_at', 'resolved_at']

class ServiceRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'request_type',
            'details',
            'file',
            'status',
            'submitted_at',
            'resolved_at',
        ]

class ServiceRequestManagementSerializer(serializers.ModelSerializer):
    """
    Serializer for customer support representatives to manage service requests.
    """

    class Meta:
        model = ServiceRequest
        fields = ['id', 'status', 'resolved_at']
        read_only_fields = ['id', 'resolved_at']  # Allow updates only to the status field

    def update(self, instance, validated_data):
        """
        Override update method to set 'resolved_at' timestamp when status is updated to 'resolved'.
        """
        status = validated_data.get('status', instance.status)
        if status == 'resolved' and instance.status != 'resolved':
            instance.resolved_at = serializers.DateTimeField().to_internal_value(
                self.context['request'].data.get('resolved_at')
            )
        instance.status = status
        instance.save()
        return instance