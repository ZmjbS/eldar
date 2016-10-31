from django.contrib import admin
from lager.models import Vara, Verd

class VaraAdmin(admin.ModelAdmin):
	list_display = ('argerd', 'fulltnafn', 'stuttnafn', 'stada', 'nytt', )
	list_editable = ('stuttnafn', 'stada')

admin.site.register(Vara, VaraAdmin)
admin.site.register(Verd)
