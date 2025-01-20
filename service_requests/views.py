from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer, ServiceRequestDetailSerializer, ServiceRequestManagementSerializer
from rest_framework import status
from .models import ServiceRequest
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from .tasks import process_service_request

from .tasks import process_service_request

class SubmitRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ServiceRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            service_request = serializer.save(customer=request.user)
            # Queue the task for processing the service request
            process_service_request.delay(service_request.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrackRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = ServiceRequest.objects.filter(customer=request.user)
        serializer = ServiceRequestSerializer(requests, many=True)
        return Response(serializer.data)

class ServiceRequestTrackingView(generics.ListAPIView):
    """
    API view to track service requests.
    Customers can view the status of their requests and details.
    """
    serializer_class = ServiceRequestDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict the service requests to the logged-in user.
        Optionally filter by request ID if provided in the query parameters.
        """
        user = self.request.user
        queryset = ServiceRequest.objects.filter(customer=user)

        # Filter by request ID if 'id' parameter is provided
        request_id = self.request.query_params.get('id', None)
        if request_id:
            queryset = queryset.filter(id=request_id)

        return queryset

class ServiceRequestManagementView(generics.RetrieveUpdateAPIView):
    """
    API view for customer support representatives to manage service requests.
    Allows updating the status and resolving requests.
    """
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestManagementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Ensure only authorized representatives can update the request.
        """
        user = self.request.user
        if not user.is_staff:  # Assuming customer support representatives have 'is_staff' set to True
            raise PermissionDenied("You do not have permission to manage service requests.")
        serializer.save()

class ServiceRequestCreateView(generics.CreateAPIView):
    """
    API view to create a new service request.
    Handles file uploads.
    """
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    parser_classes = [MultiPartParser, FormParser]  # Enable file parsing
    permission_classes = [permissions.IsAuthenticated]