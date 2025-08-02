from django.contrib import admin

# Register your models here.

from .models import Massage
from .models import Practice
from .models import Address
from .models import Openings

class MassageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",)}

admin.site.register(Massage, MassageAdmin)

class PracticeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",)}
admin.site.register(Practice, PracticeAdmin)

admin.site.register(Address)
admin.site.register(Openings)
