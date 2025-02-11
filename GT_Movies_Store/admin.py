from django.contrib import admin
from .models import Movie
from .models import Review
from django.contrib import admin
from .models import Order


admin.site.register(Movie)

admin.site.register(Review)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_price', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'status')
    ordering = ('-order_date',)

    list_editable = ('status',)  \

    fields = ('user', 'order_date', 'total_price', 'status')
    readonly_fields = ('user', 'order_date', 'total_price')  # Prevents editing user & date

