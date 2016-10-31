from django.contrib import admin
from vaktir.models import Timabil,Starfsstod,Tegund,Vakt,Felagi,Skraning

class VaktAdmin(admin.ModelAdmin):
	list_display = ('starfsstod', 'timabil', 'tegund', 'lagmark', 'hamark', )
	list_editable = ()

admin.site.register(Timabil)
admin.site.register(Starfsstod)
admin.site.register(Tegund)
admin.site.register(Vakt, VaktAdmin)
admin.site.register(Felagi)
admin.site.register(Skraning)
