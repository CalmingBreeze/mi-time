from django.contrib import admin

# Register your models here.

from .models import SiteConfig
from .models import Page
from .models import GiftCard
from .models import Bundle
from .models import Massage
from .models import Practice
from .models import Address
from .models import Openings

class MitimeAdmin(admin.AdminSite):

    ADMIN_ORDERING = (
        ('core', (
            'Practice',
            'Address',
            'Openings',
            'Massage',
            'GiftCard',
            'Bundle',
            'Page',
            'SiteConfig'
        )),
        # ('anotherapp', (
        # ))
    )

    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """

        app_dict = self._build_app_dict(request, app_label)
    
        if not app_dict:
            return
        
        NEW_ADMIN_ORDERING = []
        if app_label:
            for ao in self.ADMIN_ORDERING:
                if ao[0] == app_label:
                    NEW_ADMIN_ORDERING.append(ao)
                    break

        if not app_label:
            for app_key in list(app_dict.keys()):
                if not any(app_key in ao_app for ao_app in self.ADMIN_ORDERING):
                    app_dict.pop(app_key)
        
        app_list = sorted(
            app_dict.values(), 
            key=lambda x: [ao[0] for ao in self.ADMIN_ORDERING].index(x['app_label'])
        )
        
        for app, ao in zip(app_list, NEW_ADMIN_ORDERING or self.ADMIN_ORDERING):
            if app['app_label'] == ao[0]:
                for model in list(app['models']):
                    if not model['object_name'] in ao[1]:
                        app['models'].remove(model)
            app['models'].sort(key=lambda x: ao[1].index(x['object_name']))
        return app_list

admin_site = MitimeAdmin(name="miadmin")

admin_site.register(SiteConfig)

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",), "meta_title" : ("name",)}
admin_site.register(Page, PageAdmin)

class GiftcardAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",), "meta_title" : ("name",)}
admin_site.register(GiftCard, GiftcardAdmin)

class BundleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",), "meta_title" : ("name",)}
admin_site.register(Bundle, BundleAdmin)

class MassageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",), "meta_title" : ("name",)}
admin_site.register(Massage, MassageAdmin)

class PracticeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",), "meta_title" : ("name",)}
admin_site.register(Practice, PracticeAdmin)

admin_site.register(Address)
admin_site.register(Openings)


# admin.site.register(SiteConfig)

# class PageAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug" : ("name",)}
# admin.site.register(Page, PageAdmin)

# class MassageAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug" : ("name",)}
# admin.site.register(Massage, MassageAdmin)

# class PracticeAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug" : ("name",)}
# admin.site.register(Practice, PracticeAdmin)

# admin.site.register(Address)
# admin.site.register(Openings)
