from celery import shared_task
from .models import ServiceRequest
from django.utils.timezone import now
import time  # Simulating a delay for testing purposes

@shared_task
def process_service_request(request_id):
    """
    Asynchronous task to process service requests (e.g., mark as resolved).
    Simulates a time delay for processing.
    """
    try:
        service_request = ServiceRequest.objects.get(id=request_id)
        time.sleep(5)  # Simulating processing delay
        service_request.status = 'resolved'
        service_request.resolved_at = now()
        service_request.save()
        return f'Service Request {request_id} has been resolved.'
    except ServiceRequest.DoesNotExist:
        return f'Service Request {request_id} not found.'
