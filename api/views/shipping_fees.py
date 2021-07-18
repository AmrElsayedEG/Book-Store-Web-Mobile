from mainsite.models import shipping_fee
from rest_framework.response import Response
from rest_framework.views import APIView

class shippingFeesView(APIView):
    def get(self, request):
        if 'city' in self.request.query_params:
            fees_model = shipping_fee.objects.filter(city__iexact=self.request.query_params['city'])
            if fees_model.exists():
                fees_model = fees_model.last()
                return Response({'success' : fees_model.fees})
            fees_model = shipping_fee.objects.get(city='default')
            return Response({'success' : fees_model.fees})
        return Response({'error' : 'wrong params'}, status=400)