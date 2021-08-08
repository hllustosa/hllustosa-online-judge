from api.models import Profile
from .utils import IsAuthenticatedWith, method_permission_classes, ANY
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from .serializers import ClaimsObtainPairSerializer, UserResponseSerializer

# Create your views here.


class ClaimsTokenObtainPairView(TokenObtainPairView):
    serializer_class = ClaimsObtainPairSerializer


class UsersListView(APIView):

    @method_permission_classes((IsAuthenticatedWith(ANY),))
    def get(self, request):
        users = User.objects.all().order_by('id')

        name = request.query_params.get('name', None)
        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('pageSize', 10)

        if name is not None:
            users = users.filter(name__icontains=name)

        count = users.count()
        paginator = Paginator(users, pageSize)

        users_serializers = UserResponseSerializer(
            paginator.page(page), many=True)
        return JsonResponse({'items': users_serializers.data, 'count': count}, safe=False)


class UsersListDetailsView(APIView):

    @method_permission_classes((IsAuthenticatedWith(ANY),))
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        profile = Profile.objects.filter(user=user).first()

        if profile == None:
            type = ""
        else:
            type = 'Teacher' if profile.type == profile.TEACHER else 'Student'

        return JsonResponse({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'type': type}, safe=False)
