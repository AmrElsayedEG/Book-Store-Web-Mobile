from rest_framework.response import Response
from .hash import encode
from rest_framework.views import APIView

        
class encodeAPI(APIView):

    def post(self, request):
        if 'sec_key' in self.request.data:
            return Response({"sec_key" : encode(request.data['sec_key'])})
        return Response({'error':'Bad params'}, status=400)
