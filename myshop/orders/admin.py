from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpRequest
from django.db.models.query import QuerySet

import csv
import datetime


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def order_payment(obj: Order):
    stripe_payment_url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{stripe_payment_url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

order_payment.short_description = 'Stripe payment'

def export_to_csv(modeladmin: admin.ModelAdmin,
                  request: HttpRequest,
                  queryset: QuerySet) -> HttpResponse:
    
    options = modeladmin.model._meta
    content_disposition = f'attachment; fiename={options.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    writer = csv.writer(response)
    fields = [field for field in options.get_fields() 
              if not field.many_to_many 
              and not field.one_to_many]
    
    # Write the first row with header info
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for object in queryset:
        data_row = []
        for field in fields:
            value = getattr(object, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    
    return response
export_to_csv.short_description = 'Export to CSV'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 
                    'address', 'postal_code', 'city', 'paid',
                    order_payment ,'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]