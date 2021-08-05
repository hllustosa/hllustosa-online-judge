from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from api.models import Profile

class ClaimsObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        #try:
        token = super().get_token(user)
        profile = Profile.objects.get(user_id__exact=user.id)

        # Add custom claims
        token['id'] = user.id
        token['type'] = profile.type
        # ...

        #except:
        #    pass
        #finally:
        return token