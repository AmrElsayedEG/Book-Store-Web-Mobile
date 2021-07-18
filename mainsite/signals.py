from django.dispatch import receiver
from django.db.models.signals import post_migrate
from mainsite.models import shipping_fee, website_layout
from mainsite.apps import MainsiteConfig



##################################################
# send signal when listen to migrate on database
##################################################
@receiver(post_migrate, sender=MainsiteConfig)
def fees_migrate(sender, **kwargs):
    if not shipping_fee.objects.all().exists():
        shipping_fee(city='default',fees=50).save()
        
        
@receiver(post_migrate, sender=MainsiteConfig)
def layout_migrate(sender, **kwargs):
    if not website_layout.objects.all().exists():
        website_layout().save()
