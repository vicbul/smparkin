from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin, FilterableDjangoMpttAdmin
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin

from models import Common, CSE, APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION, test, test1, test2
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
'''

class CommonAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = ('Mandatory', {
        'fields': ['resourceType','name','parent'],
    })

    base_model = Common
    base_fieldsets = (
        GENERAL_FIELDSET,
    )

#TODO find a way to only allow creating specific resources from a specific parent node
class CombinedAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = Common
    child_models = (
        (CSE, CommonAdmin),
        (APP, CommonAdmin),
        (CONTAINER, CommonAdmin),
        (SUBSCRIPTION, CommonAdmin),
        (CONTENTINSTANCE, CommonAdmin),# custom admin allows custom edit/delete view.
    )

    list_display = ('name','actions_column',)

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',)
        }


admin.site.register(Common, CombinedAdmin)
# admin.site.register(test, TreeNodeParentAdmin)



