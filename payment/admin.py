from django.contrib import admin
from .models import Payment
import csv
from django.http import HttpResponse
# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id','user','payment_method','cost','date',)
    list_filter = ('date','payment_method',)
    search_fields = ['user__username', 'id','order_id',]

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("payments-report")
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

admin.site.register(Payment, PaymentAdmin)
