from rest_framework import generics
from django.contrib.auth.models import User
from api.serializers import RegisterSerializer
from rest_framework.response import Response

class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        reg_user = self.serializer_class(data=self.request.data)
        reg_user.is_valid(raise_exception=True)
        reg_user.save()
        return Response({"success": "Check your Email to activate your account."})