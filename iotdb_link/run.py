import pymysql
import datetime
import base64
import criotdm, ciotdm

ALL_DEVICE_INFO = {}

# iotdm ip address
httphost = "172.27.255.182"

# iotdm authentication "admin" is default
httpuser = "admin"
httppass = "admin"

# for iotdm library
rt_ae = 2
rt_container = 3
rt_contentInstance = 4

#Customer name
CUSTOMER = "makazmie"

# Application EUI
APPEUI = '0807123456789011' #"0807123456789010"
AE_PATH = CUSTOMER + "/app:" + APPEUI +"/"

# Connecting to the database
db = pymysql.connect(host='127.0.0.1',
                     user='spadmin',
                     password='spadmin',
                     db='smartparking',
                     cursorclass = pymysql.cursors.DictCursor)
cursor = db.cursor()


# Checking if data is already in iotdb_link_datafromdevices table. Adding it in case is not there.

def add_device(device):
    try:
        sql_select_device_id = "SELECT id FROM iotdb_link_device WHERE device_name = '%s'" % (str(device))
        cursor.execute(sql_select_device_id)
        dev = cursor.fetchone()
    except Exception as e:
        print 'Error accessing MySQL:', e
        return False
    if dev == None:
        print 'Device not fount. Adding new device...'
        sql_insert = "INSERT INTO iotdb_link_device (device_name, parking_slot) VALUES ('%s', 0)" % (str(device))
        cursor.execute(sql_insert)
        db.commit()
        cursor.execute(sql_select_device_id)
        new_dev = cursor.fetchone()
        return new_dev['id']
    else:
        print 'Device %s already registered.' % dev['id']
        return dev['id']

# Add the new data row in case there is not other row with same datetime for that specific device
def add_datafromdevice(dtime, data, device_id):
    print 'Trying to add device_id %s data...' % device_id
    try:
        sql_select_time = "SELECT time FROM iotdb_link_datafromdevice WHERE device_id = %s" % device_id
        cursor.execute(sql_select_time)
        dev_data = cursor.fetchall()
        if dev_data == None:
            dev_data = {}
        print 'dev_data:',dev_data
        for packet in dev_data:
            if dtime == packet['time']:
                print 'Packet time already registered.', dtime, packet['time']
                return
        print 'Adding data from device_id %s' % (device_id)
        sql_insert = "INSERT INTO iotdb_link_datafromdevice (time, data, device_id ) VALUES ('%s', '%s', %s)" \
                     % (dtime, str(data), device_id)
        cursor.execute(sql_insert)
        db.commit()
    except Exception as e:
        print 'Error accessing MySQL:', e


# get data of device which belongings to CUSTOMER APPEUI
def get_data_from_iotdm():
    connect = criotdm.connect_to_iotdm(httphost, httpuser, httppass, "http")
    ae_json = connect.retrieve(AE_PATH).json()
    print 'ae_jsom:', ae_json
    #get device list
    try:
        for dev_info in ae_json["m2m:ae"]["ch"]:
            print 'Device info:', dev_info
            ALL_DEVICE_INFO[dev_info["rn"]] = []
    except Exception as e:
        print e
        print "Exeption whcn get ae info from iotdm"

    try:
        for device in ALL_DEVICE_INFO:
            print 'device', device
            device_id = add_device(device)
            #get data list of device
            ret = connect.retrieve(AE_PATH + device + "/rx/")
            dev_json  = ret.json()
            for data in dev_json["m2m:cnt"]["ch"]:
                print 'Data: ',data
                #skip notify node
                if("notify" in data["rn"]):
                    print 'continue'
                    continue

                #get data of device
                ret = connect.retrieve(AE_PATH + device + "/rx/" + data["rn"])
                data_json = ret.json()

                print data_json
                dtime = datetime.datetime.strptime(data_json['m2m:cin']['lt'], "%Y%m%dT%H%M%S" )
                print 'dtime:', dtime, data_json['m2m:cin']['con']
                #x=base64.decodestring(data_json['m2m:cin']['con'])
                #print x
                if device_id != False:
                    add_datafromdevice(dtime, data_json['m2m:cin']['con'], device_id)


    except Exception as e:
        print e
        print "Exeption whcn get ae info from iotdm"

    finally:
        db.close()
    return

get_data_from_iotdm()
#add_device('3')
