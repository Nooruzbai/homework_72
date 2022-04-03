from django.contrib import admin

from quotes_api.models import Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'status', 'date_created']


admin.site.register(Quote, QuoteAdmin)
