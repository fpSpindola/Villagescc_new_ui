from django.contrib import admin

from relate.models import Endorsement

class EndorsementAdmin(admin.ModelAdmin):
    list_display = (
        'endorser',
        'recipient',
        'weight',
        'updated',
    )
    ordering = ('-updated',)

admin.site.register(Endorsement, EndorsementAdmin)
