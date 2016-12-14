from django.contrib import admin

from models import CSE, APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION, test

# Register your models here.

class CommonAdmin(admin.ModelAdmin):
    mandatory_fields = ['resourceName','parentID']
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
    mandatory_fields = ['resourceName','parentID','CSE_ID','CSE_Type']

class AppAdmin(CommonAdmin):
    mandatory_fields = ['resourceName','parentID','requestReachability']

class CntAdmin(CommonAdmin):
    mandatory_fields = ['resourceName','parentID']

class CinAdmin(CommonAdmin):
    exclude = ['resourceID']
    mandatory_fields = ['resourceName','parentID','content']

class SubAdmin(CommonAdmin):
    mandatory_fields = ['resourceName','parentID','notificationURI','notificationContentType','eventNotificationCriteria']

admin.site.register(CSE, CSEAdmin)
admin.site.register(APP, AppAdmin)
admin.site.register(CONTAINER, CntAdmin)
admin.site.register(CONTENTINSTANCE, CinAdmin)
admin.site.register(SUBSCRIPTION, SubAdmin)
admin.site.register(test)



