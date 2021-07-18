from mainsite.views import feedback_email
from rest_framework.response import Response
from rest_framework.views import APIView

class feedback(APIView):

    def post(self, request):
        fb_email = feedback_email(fullname=self.request.data['fullname'],
                               email=self.request.data['email'],
                               subject=self.request.data['subject'],
                               message=self.request.data['message'])
        if fb_email is True:
            return Response({'success' : 'We recieved your feedback and will get back to you soon.'})
        return Response({'error' : 'Something went wrong, Please try again'}, status=400)