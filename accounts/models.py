from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
#from social_core.utils import slugify
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from .tokens import account_activation_token
from bookstore.settings import SITE_URL
from mainsite.models import Product
from utils import CountryListChoices

class Profile(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='customer_profile')
    country = models.CharField(choices=CountryListChoices.choices,default=CountryListChoices.EGYPT,max_length=50,blank=False)
    city = models.CharField(max_length=50,default='City')
    postal_code = models.CharField(max_length=100,default='Postal Code')
    address_1 = models.CharField(max_length=100,default='Address 1')
    address_2 = models.CharField(max_length=100,default='Address 2 (street, Building)')
    phone = models.CharField(max_length=20,default='Phone')

    def __str__(self):
        return '%s' %(self.user)
        
def create_profile(sender , **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
                'user': kwargs['instance'].first_name,
                'domain': SITE_URL,
                'uid': urlsafe_base64_encode(force_bytes(kwargs['instance'].pk)),
                'token': account_activation_token.make_token(kwargs['instance']),
            })
        #text_content = strip_tags(message)
        to_email = kwargs['instance'].email
        email = EmailMultiAlternatives(
                mail_subject, 'Book Store', to=[to_email]
            )
        email.attach_alternative(message, "text/html")
        email.send()

post_save.connect(create_profile,sender=User)


class users_wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.email)

