from mainsite.models import coupon
from rest_framework.response import Response
from rest_framework.views import APIView

class CouponAPI(APIView):
    
    def get(self, request, *args, **kwargs):
        return Response({'error':'Wrong Coupon Code'})
    
    def post(self, request, *args, **kwargs):
        try:
            queryset = coupon.objects.filter(code=self.request.data['code'])
            if queryset[0].active == False:
                return Response({'error':'Coupon Code Expired'})
            prev = order.objects.filter(coupon=queryset[0],user_id=self.request.data['user_id'])
            if prev.exists():
                return Response({'error':'You already used this coupon'})
            return Response({'id':queryset[0].id,'discount_percentage':queryset[0].discount_percentage})
        except:
            return Response({'error':'Wrong Coupon Code'})