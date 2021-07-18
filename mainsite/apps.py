from django.apps import AppConfig


class MainsiteConfig(AppConfig):
    name = 'mainsite'

    def ready(self):

        # add default data
        from .signals import fees_migrate, layout_migrate
        from django.db.models.signals import post_migrate

        
        post_migrate.connect(fees_migrate, sender=self)
        post_migrate.connect(layout_migrate, sender=self)
        
