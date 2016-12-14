import sys
from cStringIO import StringIO

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete, post_save
from iotdm import iotdm_api
from iotdm.onem2m_xml_protocols import ae, container, subscription, contentinstance
from resources.models import Common, CSE, APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION
from resources.iotdm_utils import cse_provisioning
import datetime, ast

def add_to_tree(sender, instance, **kwargs):
    print 'instance', instance
    if sender == APP:
        print 'I got a App signal!',instance,instance.resourceName
        AE = ae.ae()
        AE.set_api(instance.App_ID)
        AE.set_apn(instance.AE_ID)
        AE.set_poa([instance.pointOfAccess.replace(' ','')])
        AE.set_rr(instance.requestReachability)
        process_reply(instance, AE)

    elif sender == CONTAINER:
        print 'I got a container signal!', kwargs, instance.parentID
        cnt = container.cnt()
        process_reply(instance, cnt)


    elif sender == CONTENTINSTANCE:
        print 'I got a contentinstance signal!', kwargs, instance.parentID
        cin = contentinstance.cin()
        cin.set_con(instance.content)
        process_reply(instance, cin)

    elif sender == SUBSCRIPTION:
        print 'I got a subscription signal!', kwargs, instance.parentID
        sub = subscription.sub()
        sub.set_nu([instance.notificationURI])
        sub.set_nct(instance.notificationContentType)
        sub.set_enc(ast.literal_eval(instance.eventNotificationCriteria))
        process_reply(instance, sub)

def process_reply(instance, res):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    print 'create date:',instance.creationTime
    # if instance.creationTime is None:
    res.set_rn(instance.resourceName)
    payload = res.to_JSON()
    create_res = iotdm_api.create('http://localhost:8282/'+instance.parentID, instance.resourceType, payload,
                                  origin="/django-admin", requestID="12345")
    # else: TODO Find a way to update resources that already exist in the tree
    #     res.set_rn(instance.resourceName)
    #     print 'http://localhost:8282/'+instance.previous_parentID+'/'+instance.resourceName
    #     payload = res.to_JSON()
    #     print payload
    #     update_res = iotdm_api.update('http://localhost:8282/'+instance.previous_parentID, payload,
    #                                   origin="/django-admin", requestID="12345")
    sys.stdout = old_stdout
    reply = mystdout.getvalue()
    print reply
    instance.iotdm_response = reply
    reply_dict = ast.literal_eval(reply[reply.find('{"'):])
    if reply_dict.keys()[0] == 'error':
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


def remove_from_tree(sender,  instance, **kwargs):
    print "I've got a signal pre_delete"
    if sender in [APP, CONTAINER, CONTENTINSTANCE, SUBSCRIPTION]:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        iotdm_api.delete('http://localhost:8282/'+instance.parentID+'/'+instance.resourceName)
        sys.stdout = old_stdout
        reply = mystdout.getvalue()
        print 'reply:',reply
        if reply.find('error') != -1 and instance.check_iotdm_response == True:
            raise ValidationError('Resource could not be deleted: '+instance.resourceName+': '+reply)

post_save.connect(cse_provisioning, CSE)
pre_save.connect(add_to_tree)
pre_delete.connect(remove_from_tree)