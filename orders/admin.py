from django.contrib import admin
from .models import order,OrderItem
import csv
from django.http import HttpResponse, HttpResponseRedirect
# Register your models here.

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','customer_name','city','is_paid', 'order_status', 'created', 'used_coupon', 'total_price',)
    readonly_fields = ('total_price', 'used_coupon',)
    list_filter = ('is_paid','order_status',)
    search_fields = ['user__username', 'id']
    inlines = [OrderItemAdmin,]

    actions = ["export_as_csv","Delivered_and_paid"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format("orders-report")
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

    def Delivered_and_paid(self, request, queryset):
        print(queryset)
        for i in queryset:
            i.order_status = 'Delivered'
            i.is_paid = True
            i.save()
        self.message_user(request, "Order Updated")

admin.site.register(order, OrderAdmin)
#admin.site.register(OrderItem)
