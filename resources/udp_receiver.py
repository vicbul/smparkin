import socket, requests

UDP_IP = "0.0.0.0"
UDP_PORT = 8586
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    try:
        clean_data = eval('{"stat":'+data.rsplit('{"stat":')[1].replace(' CET',''))
        r = requests.post('http://localhost:8000/admin/resources/status/', clean_data)
    except:
        clean_data = {'stat':'No data from sensors.'}
    print 'Address:', addr
    print "received message:", clean_data['stat']
