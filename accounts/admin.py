from django.contrib import admin
from .models import Profile, users_wishlist
# Register your models here.

class CustomProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city',)
    search_fields = ('user__email', 'user__first_name',)
    list_filter = ('city',)


from django.contrib.sessions.models import Session

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    
admin.site.register(Session, SessionAdmin)

admin.site.register(Profile, CustomProfileAdmin)

admin.site.register(users_wishlist)



