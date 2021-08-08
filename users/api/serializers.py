from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from .models import Profile

class ClaimsObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token['id'] = user.id
        if user.is_superuser:
            #All superusers are teachers
            token['type'] = 'T'
        else:
            try:
                profile = Profile.objects.get(user_id__exact=user.id)
                token['type'] = profile.type
            except:
                pass

        return token

class UserResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')