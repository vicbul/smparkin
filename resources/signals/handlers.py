from django.core.exceptions import ValidationError
from django.db.models.signals import pre_init, post_init, pre_save, pre_delete, post_save, post_delete
from iotdm.onem2m_xml_protocols import ae, container, subscription, contentinstance
from resources.models import Resource, test, CSE, APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION
from mptt_graph.models import GraphModel
from resources.references import longToShortDict, shortToLongDict
from SmartParking import settings
import datetime, ast, requests

if settings.CHECK_IOTDM_RESPONSE is True:
    from iotdm import iotdm_api

# TODO consider overriding save() method instead of using signals

def cse_provisioning(sender, instance, **kwargs): #cse_id='InCSE1', cse_type='IN-CSE'):
    try:
        # Update mptt_graph root node ID after provisioning CSE
        print 'Changing mptt graph node pk to', instance.pk
        resource_tree_graph = GraphModel.objects.filter(title='resources_tree')
        resource_tree_graph.update(model_pk = instance.pk, model_path = 'resources.models.CSE')
        print resource_tree_graph
        print resource_tree_graph[0].model_pk, resource_tree_graph[0].model_path
    except Exception, e:
        print 'No resources_tree graph was found:', e

    # if settings.CHECK_IOTDM_RESPONSE is True:
    cse_id = instance.CSE_ID
    cse_type = instance.CSE_Type
    url = 'http://localhost:8181/restconf/operations/onem2m:onem2m-cse-provisioning'
    headers = {'Content-Type':'application/json',
               'Accept':'application/json',
               'Authorization':'Basic YWRtaW46YWRtaW4='}
    body = {"input": {"onem2m-primitive": [{"name": "CSE_ID","value": cse_id},{"name": "CSE_TYPE","value": cse_type}]}}
    test = requests.post(url, headers=headers, json=body)

    # Creting django_sub
    django_sub = SUBSCRIPTION(name='django_sub', parent=instance)
    django_sub.save()

    return test.json()

update_iotdm_resource_fields = {
    #'common':['labels'],# 'announceTo', 'announcedAttribute'],
    # CSE:['CSE_ID', 'CSE_Type', 'supportedResourceType', 'pointOfAccess', 'nodeLink', 'e2eSecInfo', \
    #      'notificationCongestionPolicy'],
    APP:['appName', 'pointOfAccess'],
    CONTAINER:['accessControlPolicyIDs','labels'],
    CONTENTINSTANCE:['content'],
    SUBSCRIPTION:['notificationURI','notificationContentType','eventNotificationCriteria'],
}

create_iotdm_resource_fields = {
    APP:['requestReachability', 'App_ID'],
    CONTAINER:[],
    CONTENTINSTANCE:['content'],
    SUBSCRIPTION:['notificationURI','notificationContentType','eventNotificationCriteria'],
}

def model_to_iotdm_api(sender, **kwargs):

    if sender == APP:
        return ae.ae(**kwargs)
    elif sender == CONTAINER:
        return container.cnt(**kwargs)
    elif sender == CONTENTINSTANCE:
        return contentinstance.cin(**kwargs)
    elif sender == SUBSCRIPTION:
        return subscription.sub(**kwargs)
    else:
        return None

# TODO accomodate all possible fields (check what fields are arrays)
# TODO Consider not using python API
def add_to_tree(sender, instance, created, **kwargs):
    if sender in [APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION]:
        if created is True:
            target_fields = create_iotdm_resource_fields[sender]
        else:
            target_fields = update_iotdm_resource_fields[sender]

        d = {}
        for f in target_fields:
            print 'attribute', str(getattr(instance, f))
            if len(str(getattr(instance, f)))>0 and str(getattr(instance, f))[0] in ['[','{']:
                d[longToShortDict[f]] = eval(getattr(instance, f))
            else:
                d[longToShortDict[f]] = getattr(instance, f)
        print 'update dictionary', d

        res = model_to_iotdm_api(sender, **d)
        process_reply(sender, instance, res, created)


# DEPRECATED: new add_to_tree function handles models and fields dinamically
def add_to_tree_DEPRECATED(sender, instance, created, **kwargs ):
    print 'instance', instance
    if sender == APP:
        print 'I got a App signal!'#,instance,instance.name, 'Is new = '+str(created)
        AE = ae.ae()
        AE.set_api(instance.App_ID)
        AE.set_apn(instance.AE_ID)
        AE.set_poa([instance.pointOfAccess.replace(' ','')])
        AE.set_rr(instance.requestReachability)
        process_reply(sender, instance, AE, created)

    elif sender == CONTAINER:
        print 'I got a container signal!'#, kwargs
        cnt = container.cnt()
        process_reply(sender, instance, cnt, created)


    elif sender == CONTENTINSTANCE:
        print 'I got a contentinstance signal!'#, kwargs
        cin = contentinstance.cin()
        cin.set_con(instance.content)
        process_reply(sender, instance, cin, created)

    elif sender == SUBSCRIPTION:
        print 'I got a subscription signal!'#, kwargs
        sub = subscription.sub()
        sub.set_nu([instance.notificationURI])
        sub.set_nct(instance.notificationContentType)
        sub.set_enc(eval(instance.eventNotificationCriteria))
        process_reply(sender, instance, sub, created)


def process_reply(sender, instance, res, created):

    # old_stdout = sys.stdout
    # sys.stdout = mystdout = StringIO()
    parent_uri = '/'.join([ancestor.name for ancestor in instance.get_ancestors()])


    if created == True:# or created == False:
        print 'Creating new resource'
        res.set_rn(instance.name)
        payload = res.to_JSON()
        # I have modified the IoTdm python API to return just the JSON data
        reply = iotdm_api.create(settings.IOTDM_SERVER+parent_uri, instance.resourceType, payload,
                                 origin=None, requestID=None)


    # TODO iotdm_resource_name no longer needed since name cannot be changed on IoTdm
    else:
        print 'Updating resource', instance.iotdm_resource_name
        # res.set_rn(instance.iotdm_resource_name)
        payload = res.to_JSON()
        print 'Payload', payload
        reply = iotdm_api.update(settings.IOTDM_SERVER+parent_uri+'/'+instance.name, payload,
                                 origin=None, requestID=None)

    # # sys.stdout = old_stdout
    # # reply = mystdout.getvalue()
    #
    # # Using eval() to convert the JSON string into a python dictionary
    # print 'add_resource_reply', reply
    # instance.iotdm_response = reply
    # reply_dict = eval(reply)#ast.literal_eval(reply)#[reply.find('{"'):])
    # if reply.find('error') != -1: # TODO design a beter way to handle IoTdm errors
    #     if created == True:
    #         print 'Error found while adding the resource.'
    #         # if created ==True:
    #         pre_delete.disconnect(remove_from_tree)
    #         instance.delete()
    #         pre_delete.connect(remove_from_tree)
    #         raise ValidationError(reply_dict[reply_dict.keys()[0]])
    #         return
    #     else:
    #         print 'Error found while updating the resource. The resources has not been updated on IoTdm.'
    #         raise ValidationError(reply_dict[reply_dict.keys()[0]])
    #         return
    #
    # # After saving the new created resource on IoTdm, update ct and ri on django via queryset
    # if created == True:#instance.creationTime is None:
    #     sender.objects.filter(pk=instance.pk).update(creationTime = parse_date(reply_dict[reply_dict.keys()[0]]['ct']))
    # if instance.resourceID == '':
    #     sender.objects.filter(pk=instance.pk).update(resourceID = reply_dict[reply_dict.keys()[0]]['ri'])
    #
    # # After updating the new/existing resource on IoTdm, update lt on django via queryset
    # sender.objects.filter(pk=instance.pk).update(lastModifiedTime = parse_date(reply_dict[reply_dict.keys()[0]]['lt']))

def save_iotdm_resource_name(sender, instance, **kwargs):
    if sender in [CSE, APP, CONTAINER, SUBSCRIPTION, CONTENTINSTANCE]:
        # sender.objects.filter(pk=instance.pk).update(iotdm_resource_name = instance.name)
        print 'Storing iotdm_resource_name', instance.name
        instance.iotdm_resource_name = instance.name


def parse_date(date):
    # parse ISO 8601/RFC 3339 to datetime
    print 'Parsing date', date
    date = datetime.datetime.strptime(date, "%Y%m%dT%H%M%S" )
    return date

#TODO get_ancestors method returns an empty queryset when called from pre_delete signal receivers. It returns a list without immediate parent
#TODO when deleting multiple levels objects it may occur that a parent is deleted before the child and be removed from IoTdm. This would prevent django object from being deleted
def remove_from_tree(sender,  instance, **kwargs):
    print "I've got a signal pre_delete for", instance
    if sender in [APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION]:
        print 'Resource is valid.'
        res_uri = '/'.join([ancestor.name for ancestor in instance.parent.get_ancestors(include_self=True)])+'/'+instance.name
        print 'res_uri',res_uri
        reply = iotdm_api.delete(settings.IOTDM_SERVER+res_uri)
        print 'delete_resource_reply:',reply
        if reply.find('error') != -1:
            if reply.find('Resource target URI not found'):
                return
            else:
                raise ValidationError('Resource could not be deleted: '+instance.name+': '+reply)
                return
    elif sender is CSE:
        print 'CSE root resource cannot be deleted from IoTdm. Please restart IoTdm to re-provisionning CSE details.'

if settings.CHECK_IOTDM_RESPONSE is True:
    # post_init.connect(save_iotdm_resource_name)
    post_save.connect(cse_provisioning, CSE)
    post_save.connect(add_to_tree)
    pre_delete.connect(remove_from_tree)
