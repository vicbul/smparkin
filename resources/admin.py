from django.contrib import admin
from django.contrib.admin import ModelAdmin
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin

from models import *

# ACTIONS
# TODO add an action to build the existing tree on iotdm


# Register your models here.
# TODO create a button in the admi panel to re-build the tree ( for r in Resource.objects.all(): r.save() )
# TODO Show what kind of resource is every tree entry in the admin panel (NAME / TYPE / ACTIONS)

class CommonAdmin(PolymorphicMPTTChildModelAdmin):
    base_model = Resource
    readonly_fields = ['resourceType']
    mandatory_fields = ['resourceType','name','parent']
    # This method allows to sear for the parent in the change_list tree (opened as a popup)
    raw_id_fields = ['parent',]
    # Allow saving a given resource as another one
    save_as = True
    save_as_continue = False

    search_fields = ['name',]

    def __init__(self, *args, **kwargs):
        super(CommonAdmin, self).__init__(*args, **kwargs)
        self.list_of_fields = self.get_fields(self)#[f.name for f in APP._meta.get_fields()]#
        #print len(self.list_of_fields), self.list_of_fields
        optional_fields = [f for f in self.list_of_fields if f not in set(self.mandatory_fields)] #best performance and keeps order
        # Using base_fieldsets instead of fieldsets for Polymorphic models)
        self.base_fieldsets = [
            ['Mandatory', {'fields': self.mandatory_fields}],
            ['optional', {
                'classes': ['collapse', 'bold'],
                'fields': optional_fields}],
        ]
    # Here you can add read only fields for existing objects you want to update
    def get_readonly_fields(self, request, obj=None):
        if obj:
            # TODO add all fields that cannot be updated on IoTdm
            return self.readonly_fields + ['name']
        return self.readonly_fields


class CSEAdmin(CommonAdmin):
    base_model = CSE
    mandatory_fields = ['resourceType','name','CSE_ID','CSE_Type','parent']


class AppAdmin(CommonAdmin):
    base_model = APP
    mandatory_fields = ['resourceType','name','requestReachability','parent']


class CntAdmin(CommonAdmin):
    base_model = CONTAINER
    mandatory_fields = ['resourceType','name','parent']


class CinAdmin(CommonAdmin):
    base_model = CONTENTINSTANCE
    # exclude = ['resourceID']
    mandatory_fields = ['resourceType','name','content','parent']


class SubAdmin(CommonAdmin):
    base_model = SUBSCRIPTION
    mandatory_fields = ['resourceType','name','notificationURI','notificationContentType','eventNotificationCriteria','parent']


class CombinedAdmin(PolymorphicMPTTParentModelAdmin):
    # To define/disable actions dropdown menu
    actions = None

    base_model = Resource
    child_models = (
        (CSE, CSEAdmin),
        (APP, AppAdmin),
        (CONTAINER, CntAdmin),
        (SUBSCRIPTION, SubAdmin),
        (CONTENTINSTANCE, CinAdmin),# custom admin allows custom edit/delete view.
    )

    list_display = ('name', 'actions_column')

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',
                    'resources/tree.css'),
        }
        # js = ('https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js',
        #       'resources/view_tree.js',
        # )


class GatewayStatsAdmin(ModelAdmin):
    list_display = ["mac","time","latitude","longitude","altitude","rxPacketsReceived","rxPacketsReceivedOK","txPacketsReceived","txPacketsEmitted","customData"]
    list_per_page = 500


class GatewayRxAdmin(ModelAdmin):
    list_display = ['date',"rxInfo","phyPayload"]


class AppDataAdmin(ModelAdmin):
    list_display = ['date','devEUI',"data","data_decoded"]

# class StatusAdmin(ModelAdmin):
#     list_display = ["time","lati","long","alti","rxnb","rxok","rxfw","ackr","dwnb","txnb"]

admin.site.register(Resource, CombinedAdmin)
admin.site.register(GatewayStats, GatewayStatsAdmin)
admin.site.register(GatewayRx, GatewayRxAdmin)
admin.site.register(AppData, AppDataAdmin)
# admin.site.register(test, TreeNodeParentAdmin)



