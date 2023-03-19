from django.urls import path
from .views import TestListCreateAPIView, TestRetrieveUpdateDestroyAPIView, RefreshTokenView


urlpatterns = [
    path('users/', TestListCreateAPIView.as_view(), name='test_list_create'),
    path('users/<int:pk>/', TestRetrieveUpdateDestroyAPIView.as_view(), name='test_retrieve_update_destroy'),
    path('users/login', RefreshTokenView.as_view(), name='test_list_create'),
    
]