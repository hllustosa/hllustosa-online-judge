from django.contrib import admin
from django.urls import path
from django.conf.urls import url 
from api.views import ClaimsTokenObtainPairView, UsersListView, UsersListDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', ClaimsTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', ClaimsTokenObtainPairView.as_view(), name='token_refresh'),
    path('api/users/all/', UsersListView.as_view(), name='users_list'),
    url(r'^api/users/(?P<pk>.*)$', UsersListDetailsView.as_view(), name='users_details'),
]
