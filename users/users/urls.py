from django.contrib import admin
from django.urls import path
from api.views import ClaimsTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', ClaimsTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', ClaimsTokenObtainPairView.as_view(), name='token_refresh'),
]
