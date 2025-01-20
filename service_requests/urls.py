from django.urls import path
from .views import SubmitRequestView, TrackRequestsView, ServiceRequestTrackingView, ServiceRequestManagementView

urlpatterns = [
    path('submit/', SubmitRequestView.as_view(), name='submit_request'),
    path('track/', ServiceRequestTrackingView.as_view(), name='service-request-tracking'),
    path('manage/<int:pk>/', ServiceRequestManagementView.as_view(), name='service-request-manage'),
    # path('track/', TrackRequestsView.as_view(), name='track_requests'),
]
