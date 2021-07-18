from rest_framework.response import Response
from orders.views import order_info_email
from rest_framework.views import APIView


class OrderEmailAPI(APIView):

    def post(self, request):
        if 'orderid' in self.request.data:
            order_info_email(request.data['orderid'])
            return Response({"success" : "Order info sent to your Email."})
        return Response({'error':'Bad params'}, status=400)