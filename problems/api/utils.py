from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, authentication

from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import User

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES
TEACHER = "teacher"
STUDENT = "student"
ANY = "any"

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


class JWTAuthentication():

    www_authenticate_realm = 'api'
    media_type = 'application/json'

    def authenticate(self, request, needed_claim):
        header = self.get_header(request)
        if header is None:
            return False

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return False

        validated_token = self.get_validated_token(raw_token)
        if needed_claim != None:
            return needed_claim == validated_token.payload['type']

        return True

    def get_user_id(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return validated_token.payload['id']

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def get_header(self, request):

        header = request.META.get(api_settings.AUTH_HEADER_NAME)

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):

        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                _('Authorization header must contain two space-delimited values'),
                code='bad_authorization_header',
            )

        return parts[1]

    def get_validated_token(self, raw_token):

        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })


class IsStudent():

    def has_permission(self, request, view):
        authetication = JWTAuthentication()
        return authetication.authenticate(request, needed_claim="S")


class IsTeacher():

    def has_permission(self, request, view):
        authetication = JWTAuthentication()
        return authetication.authenticate(request, needed_claim="T")


class IsAny():

    def has_permission(self, request, view):
        authetication = JWTAuthentication()
        return authetication.authenticate(request, needed_claim=None)


class DenyAll():

    def has_permission(self, request, view):
        return False


def IsAuthenticatedWith(type):

    if type == TEACHER:
        return IsTeacher
    elif type == STUDENT:
        return IsStudent
    elif type == ANY:
        return IsAny
    else:
        DenyAll
