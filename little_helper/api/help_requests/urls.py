from django.urls import path

from .views import *


urlpatterns = [
    path('requests/', HelpRequestListCreateView.as_view(), name='request-list-create'),
    path('requests/<int:pk>/', HelpRequestRetrieveUpdateDestroyView.as_view(), name='request-detail'),
    path('requests/mine/', MyHelpRequestsListView.as_view(), name='my-requests'),
    path('requests/<int:pk>/close/', CloseHelpRequestView.as_view(), name='close-request'),
]
