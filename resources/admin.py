from django.contrib import admin
from mptt.admin import MPTTModelAdmin
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
'''

class ResourceAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = ('Mandatory', {
        'fields': ['resourceType','name','parent'],
    })

    base_model = Resource
    base_fieldsets = (
        GENERAL_FIELDSET,
    )

class CombinedAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = Resource
    child_models = (
        (CSE, ResourceAdmin),
        (APP, ResourceAdmin),
        (CONTAINER, ResourceAdmin), #TODO fix filtering by container. Now it raises a ValueError sometimes (not in depth-first order)
        (SUBSCRIPTION, ResourceAdmin),
        (CONTENTINSTANCE, ResourceAdmin),# custom admin allows custom edit/delete view.
    )

    list_display = ('name','actions_column',)

    class Media:
        css = {
            'all': ('admin/treenode/admin.css', 'resources/tree.css'),
        }
        js = ('https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js',
              'resources/view_tree.js',
        )


admin.site.register(Resource, CombinedAdmin)
# admin.site.register(test, TreeNodeParentAdmin)



