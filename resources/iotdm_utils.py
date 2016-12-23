import requests
import mptt_graph


def cse_provisioning(sender, instance, **kwargs): #cse_id='InCSE1', cse_type='IN-CSE'):
    cse_id = instance.CSE_ID
    cse_type = instance.CSE_Type
    url = 'http://localhost:8181/restconf/operations/onem2m:onem2m-cse-provisioning'
    headers = {'Content-Type':'application/json',
               'Accept':'application/json',
               'Authorization':'Basic YWRtaW46YWRtaW4='}
    body = {"input": {"onem2m-primitive": [{"name": "CSE_ID","value": cse_id},{"name": "CSE_TYPE","value": cse_type}]}}
    test = requests.post(url, headers=headers, json=body)
    return test.json()

def get_resource_tree():
    url = 'http://localhost:8282/InCSE1?fu=1'
    headers = {'Content-Type':'application/json',
               'X-M2M-Origin':'django-admn',
               'X-M2M-RI':'12345'}
    test = requests.get(url, headers=headers)
    if str(test.json()).find('error'):
        print test.json()
    return test.json()

def build_resource_tree(child_parent):
    more_children = True if len(child_parent) > 0 else False
    pn = child_parent['None']['rn']
    pi = child_parent['None']['ri']
    while more_children:
        parent_processed = 1
        for child in child_parent[pi]:
            pn = pn+child['rn']


#cse_provisioning()

# resource_tree = get_resource_tree()
# child_parent = {}
# for r in resource_tree:
#     #print r
#     res = r.values()[0]
#     res_ri = res['ri']
#     if r.keys()[0] != 'm2m:cb':
#         #res_grandpa = '/'.join(res['pi'].split('/')[0:-1])
#         res_pi = res['pi'].split('/')[-1]
#     else:
#         #res_grandpa = '/'
#         res_pi = None
#
#     if res_pi not in child_parent.keys():
#         child_parent[res_pi] = [r]
#     else:
#         child_parent[res_pi].append(r)
#
# for p in child_parent:
#     print p, child_parent[p]