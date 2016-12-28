from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin, FilterableDjangoMpttAdmin
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin

from models import Resource, CSE, APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION, test, test1, test2

# Register your models here.

'''
# The common admin functionality for all derived models:

class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = (None, {
        'fields': ('parent', 'name'),
    })

    base_model = test
    base_fieldsets = (
        GENERAL_FIELDSET,
    )


# Optionally some custom admin code

class TextNodeAdmin(BaseChildAdmin):
    pass


# Create the parent admin that combines it all:

class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = test
    child_models = (
        (test1, BaseChildAdmin),
        (test2, TextNodeAdmin),  # custom admin allows custom edit/delete view.
    )

    list_display = ('name', 'actions_column',)

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',)
        }

class ResourceAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = ('Mandatory', {
        'fields': ['resourceType','name','parent'],
    })

    base_model = Resource
    base_fieldsets = (
        GENERAL_FIELDSET,
    )
'''

def del_button(self, obj):
    return

class CommonAdmin(admin.ModelAdmin):
    readonly_fields = ['resourceType']
    mandatory_fields = ['resourceType','name','parent']
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
    mandatory_fields = ['resourceType','name','CSE_ID','CSE_Type','parent']


class AppAdmin(CommonAdmin):
    mandatory_fields = ['resourceType','name','requestReachability','parent']


class CntAdmin(CommonAdmin):
    mandatory_fields = ['resourceType','name','parent']


class CinAdmin(CommonAdmin):
    exclude = ['resourceID']
    mandatory_fields = ['resourceType','name','content','parent']

class SubAdmin(CommonAdmin):
    mandatory_fields = ['resourceType','name','notificationURI','notificationContentType','eventNotificationCriteria','parent']


class CombinedAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = Resource
    child_models = (
        (CSE, CSEAdmin),
        (APP, AppAdmin),
        (CONTAINER, CntAdmin), #TODO fix filtering by container. Now it raises a ValueError (not in depth-first order)
        (SUBSCRIPTION, SubAdmin),
        (CONTENTINSTANCE, CinAdmin),# custom admin allows custom edit/delete view.
    )


    list_display = ('name','actions_column',)

    # def resource_type(self, obj):
    #     return ('%s' % type(obj).__name__).lower()
    # resource_type.short_description = 'Resource Type'

    class Media:
        css = {
            'all': ('admin/treenode/admin.css', 'resources/tree.css'),
        }
        js = ('https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js',
              'resources/view_tree.js',
        )

admin.site.register(Resource, CombinedAdmin)
# admin.site.register(test, TreeNodeParentAdmin)



