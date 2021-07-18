from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile
from rest_framework.authtoken.models import Token

class ProfileAPI(generics.RetrieveUpdateAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user_id'
    def get_queryset(self):
      user_token = Token.objects.get(key = self.request.query_params.get('token'))
      userid = user_token.user_id
      queryset = Profile.objects.filter(user_id=userid)
      return queryset


class UserAPI(generics.RetrieveUpdateAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    def get_queryset(self):
      user_token = Token.objects.get(key = self.request.query_params.get('token'))
      userid = user_token.user_id
      queryset = User.objects.filter(id=userid)
      return queryset