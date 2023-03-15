from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import *

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', AuthUserRegistrationView.as_view(), name='register'),
    path('register/<int:id>/', AuthUserRegistrationView.as_view(), name='register'),
    path('login/', AuthUserLoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('job/', JobCreateView.as_view(), name="jobs"),
    path('job/<int:pk>/', JobRetrieveUpdateDestroyAPIView.as_view(), name="companys"),
    path('company/', CompanyCreateView.as_view(), name="job"),
    path('company/<int:pk>/', CompanyRetrieveUpdateAPIView.as_view(), name="company"),
    path('jobtype/', JobTypeView.as_view(), name="jobtype"),
    path('vehicle/', VehicleListCreateView.as_view(), name="vehicle"),
]