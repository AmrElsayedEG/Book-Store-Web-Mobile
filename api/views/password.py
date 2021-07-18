from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import BadHeaderError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        data = request.POST['email']
        associated_users = User.objects.filter(Q(email=data))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "password/password_reset_subject.html"
                c = {
					    "email":user.email,
					    'domain':settings.SITE_URL,
					    'site_name': 'TriTlas | Egypt',
					    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
					    "user": user,
					    'token': default_token_generator.make_token(user),
				    }
                email = render_to_string(email_template_name, c)
                try:
                    msg = EmailMultiAlternatives(subject, 'Book Store', to=[user.email])
                    msg.attach_alternative(email, "text/html")
                    msg.send()
                    return JsonResponse({"success" : "An email has been sent to you"}, safe=False)
                except BadHeaderError:
                    return JsonResponse({"error" : "Error, Please Try Again!"}, status=400, safe=False)
        else:
            return JsonResponse({"error" : "An account with this email not found."}, status=400, safe=False)
    return JsonResponse("404 Not Found", safe=False)




@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('password1')
        token = request.POST.get('token')
        user_token = Token.objects.get(key = token)
        userid = user_token.user_id
        u = User.objects.get(id=userid)
        check = check_password(u,old_password)
        if check:
            u.set_password(new_password)
            u.save()
            return JsonResponse({'success':'Password Changed'}, safe=False)
        else:
            return JsonResponse({'error':'Your old password is wrong'}, status=400, safe=False)
    else:
        return JsonResponse("404 Not Found", safe=False)

def check_password(user_model,old_password):
    return user_model.check_password(old_password)