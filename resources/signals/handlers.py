import sys
from cStringIO import StringIO
import mptt

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_init, post_init, pre_save, pre_delete, post_save, post_delete
from iotdm import iotdm_api
from iotdm.onem2m_xml_protocols import ae, container, subscription, contentinstance
from resources.models import Resource, test, CSE, APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION
from resources.iotdm_utils import cse_provisioning
import datetime, ast


def add_to_tree(sender, instance, created, **kwargs):
    print 'instance', instance
    if sender == APP:
        print 'I got a App signal!',instance,instance.name, 'Is new = '+str(created)
        AE = ae.ae()
        AE.set_api(instance.App_ID)
        AE.set_apn(instance.AE_ID)
        AE.set_poa([instance.pointOfAccess.replace(' ','')])
        AE.set_rr(instance.requestReachability)
        process_reply(instance, AE, created)

    elif sender == CONTAINER:
        print 'I got a container signal!', kwargs
        cnt = container.cnt()
        process_reply(instance, cnt, created)


    elif sender == CONTENTINSTANCE:
        print 'I got a contentinstance signal!', kwargs
        cin = contentinstance.cin()
        cin.set_con(instance.content)
        process_reply(instance, cin, created)

    elif sender == SUBSCRIPTION:
        print 'I got a subscription signal!', kwargs
        sub = subscription.sub()
        sub.set_nu([instance.notificationURI])
        sub.set_nct(instance.notificationContentType)
        sub.set_enc(ast.literal_eval(instance.eventNotificationCriteria))
        process_reply(instance, sub, created)


def process_reply(instance, res, created):
    if instance.check_iotdm_response == False:
        return
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    parent_uri = '/'.join([ancestor.name for ancestor in instance.get_ancestors()])
    print 'created:', created, parent_uri
    # if instance.creationTime is None:
    res.set_rn(instance.name)
    payload = res.to_JSON()
    create_res = iotdm_api.create('http://10.48.18.34:8282/'+parent_uri, instance.resourceType, payload,
                                  origin="/django-admin", requestID="12345")
    # else: TODO Find a way to update resources that already exist in the tree
    #     res.set_rn(instance.name)
    #     print 'http://localhost:8282/'+instance.previous_parentID+'/'+instance.name
    #     payload = res.to_JSON()
    #     print payload
    #     update_res = iotdm_api.update('http://localhost:8282/'+instance.previous_parentID, payload,
    #                                   origin="/django-admin", requestID="12345")
    sys.stdout = old_stdout
    reply = mystdout.getvalue()
    print reply
    instance.iotdm_response = reply
    reply_dict = ast.literal_eval(reply[reply.find('{"'):])
    if reply.find('error') != -1: # TODO design a beter way to handle IoTdm errors
        if created ==True:
            instance.delete()
        raise ValidationError(reply_dict[reply_dict.keys()[0]])
        return
    if instance.creationTime is None:
        instance.creationTime = parse_date(reply_dict[reply_dict.keys()[0]]['ct'])
    instance.lastModifiedTime = parse_date(reply_dict[reply_dict.keys()[0]]['lt'])
    instance.full_clean()


def parse_date(date):
    # parse ISO 8601/RFC 3339 to datetime
    date = datetime.datetime.strptime(date, "%Y%m%dT%H%M%S" )
    return date

#TODO get_ancestors method returns an empty queryset when called from pre_delete signal receivers. It returns a list without immediate parent
def remove_from_tree(sender,  instance, **kwargs):
    print "I've got a signal pre_delete for", instance
    if sender in [APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION]:
        # res_uri = '/'.join([ancestor.name for ancestor in instance.get_ancestors(include_self=True)])
        res_parent = sender.objects.get(name=instance.parent) # this is a workaround pulling parent object instead
        res_uri = '/'.join([ancestor.name for ancestor in res_parent.get_ancestors(include_self=True)])+'/'+instance.name
        print 'uri:', res_uri
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        iotdm_api.delete('http://localhost:8282/'+res_uri)
        sys.stdout = old_stdout
        reply = mystdout.getvalue()
        print 'reply:',reply
        if reply.find('error') != -1 and instance.check_iotdm_response == True:
            raise ValidationError('Resource could not be deleted: '+instance.name+': '+reply)
            return

post_save.connect(cse_provisioning, CSE)
post_save.connect(add_to_tree)
pre_delete.connect(remove_from_tree)
