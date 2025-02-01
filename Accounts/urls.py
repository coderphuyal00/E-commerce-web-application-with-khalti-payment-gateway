from django.contrib import admin
from django.urls import path,include
from .views import UserProfile,updateUserDetails
urlpatterns = [
    path('accounts/user-details/',UserProfile.as_view(),name='user-details'),
    path('accounts/edit-user-details/',updateUserDetails,name='edit-user-details'),
]