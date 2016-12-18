from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from models import Common, CSE, APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION, test

# Register your models here.

class CommonAdmin(admin.ModelAdmin):
    mandatory_fields = ['name','parent']
    def __init__(self, *args, **kwargs):
        super(CommonAdmin, self).__init__(*args, **kwargs)
        self.list_of_fields = self.get_fields(self)#[f.name for f in APP._meta.get_fields()]#
        #print len(self.list_of_fields), self.list_of_fields
        optional_fields = [f for f in self.list_of_fields if f not in set(self.mandatory_fields)] #best performance and keeps order
        self.fieldsets = [
            ['Mandatory', {'fields': self.mandatory_fields}],
            ['optional', {
                'classes': ['collapse', 'bold'],
                'fields': optional_fields}],
        ]

class CSEAdmin(CommonAdmin):
    readonly_fields = ['resourceType']
    mandatory_fields = ['resourceType','name','CSE_ID','CSE_Type','parent']

class AppAdmin(CommonAdmin):
    readonly_fields = ['resourceType']
    mandatory_fields = ['resourceType','name','requestReachability','parent']

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'parent':
    #         kwargs['queryset'] = Common.objects.filter(resourceType = 5)
    #     return super(AppAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class CntAdmin(CommonAdmin):
    readonly_fields = ['resourceType']
    mandatory_fields = ['resourceType','name','parent']

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'parent':
    #         kwargs['queryset'] = Common.objects.filter(resourceType = 2)
    #     return super(CntAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class CinAdmin(CommonAdmin):
    exclude = ['resourceID']
    readonly_fields = ['resourceType']
    mandatory_fields = ['resourceType','name','content','parent']

class SubAdmin(CommonAdmin):
    mandatory_fields = ['resourceType','name','notificationURI','notificationContentType','eventNotificationCriteria','parent']

admin.site.register(CSE, CSEAdmin)
admin.site.register(APP, AppAdmin)
admin.site.register(CONTAINER, CntAdmin)
admin.site.register(CONTENTINSTANCE, CinAdmin)
admin.site.register(SUBSCRIPTION, SubAdmin)
admin.site.register(test)



