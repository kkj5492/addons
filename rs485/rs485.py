import serial
import threading
import queue
import time
import paho.mqtt.client as mqtt

host = '192.168.101.110'
port = 8899

read_buffer = queue.Queue(10000);
current_status = {}

LIGHT=32
LIVINGROOM = 1
ROOM1 = 2
GUESTROOM = 3
ROOM2 = 4
ROOM3 = 5
HALLWAY = 6
STATUS_ON=1
STATUS_OFF=0
ALL_DEVICE=1
CURRENT_STATUS=0
CHANGE=16
SW_VERSION = 'CVNET SOCKET'



def send_to_mqtt(room,device, device_number,command, value):
    mqtt_client.publish('{}/{}/{}/{}'.format(room,device,device_number,command), value)

def light_device_discovery():
    for i in range(1,8):
        mqtt_client.subscribe('livingroom/light/' +str(i)+'/status')
        mqtt_client.subscribe('livingroom/light/'+str(i)+'/command')
                        
def device_discovery():
    light_device_discovery()

def send_to_device(room,device,device_number,value):
    if value == 'ON':
        data = get_livingroom_light_request_data(device_number,1)
    else:
        data = get_livingroom_light_request_data(device_number,0)
        
    send_data(data)
    
def on_message(client, obj, msg):
    topic_list = msg.topic.split('/')
    value = msg.payload.decode()
    if topic_list[3] == 'command':
        send_to_device(topic_list[0],topic_list[1],int(topic_list[2]),value)
        
def on_publish(client, obj, mid):
    print("Publish: {}".format(str(mid)))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: {} {}".format(str(mid),str(granted_qos)))

def on_connect(client, userdata, flags, rc):
    print('[MQTT] {} :'.format(rc))
    device_discovery()

def connect_mqtt():
        mqtt_client = mqtt.Client()
        mqtt_client.on_message = on_message
        mqtt_client.on_subscribe =on_subscribe
        mqtt_client.on_connect = on_connect
        mqtt_client.username_pw_set('mqtt', 'mqtt')
        mqtt_client.connect('192.168.101.45', 1883, 60)
        mqtt_client.loop_start()
        return mqtt_client

def connect_server():     
    try:
        client = serial.Serial('COM7', 9600, timeout=None)
        if client.isOpen():
            client.bytesize = 8
            client.stopbits = 1
            client.autoOpen = False
    except Exception as e:
        print('시리얼포트에 연결할 수 없습니다.[{}]'.format(e))
    return client
    
def send_data(data):
    print('Send Data',data)
    socket_client.write(bytearray.fromhex(data))

def get_check_sum(data):
    checkSum = 0
    for i in data:
        checkSum += i
    return checkSum

def sum_to_hex(number1, number2):
    return '{:02x}'.format(number1 + number2)
    
def get_request_data(room,device,device_number,order, value):
    deviceCode = sum_to_hex(room,device)
    orderCode = sum_to_hex(device_number,order)
    StatusCode = sum_to_hex(value,0)
    data = '20' + deviceCode + '01' + orderCode + StatusCode + '00' + '00' + '00' + '00' + '00' + '00' + '00'  
    checkSum = get_check_sum(bytearray.fromhex(data))
    data = 'f7' + data + '{:02x}'.format(checkSum) + 'aa'
    return data

def get_livingroom_light_request_data(device_number, value=0):
    return get_request_data(LIVINGROOM,LIGHT,device_number,CHANGE,value)

def get_livingroom_status_request_data(device):
    return get_request_data(LIVINGROOM,device,ALL_DEVICE,CURRENT_STATUS,0)

def get_light_status_request_data(room):
    return get_request_data(room,LIGHT,ALL_DEVICE,CURRENT_STATUS,0)


def send_livingroom_status_request_data():
    livingroomStatus = []
    livingroomStatus.append(get_livingroom_status_request_data(LIGHT))
    for x in livingroomStatus:
        send_data(x)
        
def send_light_status_request_data():
    lightStatus = []
    lightStatus.append(get_light_status_request_data(LIVINGROOM))
    lightStatus.append(get_light_status_request_data(ROOM1))
    lightStatus.append(get_light_status_request_data(GUESTROOM))
    lightStatus.append(get_light_status_request_data(ROOM2))
    lightStatus.append(get_light_status_request_data(ROOM3))
    lightStatus.append(get_light_status_request_data(HALLWAY))
    for x in lightStatus:
        send_data(x)
    

def polling_data():
    threading.Timer(300, polling_data).start()
    logtime = time.strftime("%H:%M:%S",time.localtime())
    print ('[{}] 데이터 풀링 시작'.format(logtime))
    send_light_status_request_data()


            
def read_data():
    while True:
        try:
            if socket_client.readable():
                data = socket_client.read()

                if not data:
                    socket_client.close()
                    read_buffer.put(None)
                    break
                read_buffer.put(data.hex());
        except Exception as e:
            print('ERROR ',e)

def update_current_status(packet):
    head = ''.join(packet[0:4])
    newStatus = ''.join(packet[5:13])
    oldStatus = current_status.get(head)
    if newStatus == oldStatus:
        return False
    else:
        current_status[head] =newStatus
        return True
            

def process_data_to_mqtt(packet):
    if packet[2] == '01': 
        if update_current_status(packet):        
            if packet[3] == '21':
                packet_data = packet[5:12]
                index=1
                for value in packet_data:
                    if value == '01':
                        send_to_mqtt('livingroom','light',str(index),'status','ON')
                    else :
                        send_to_mqtt('livingroom','light',str(index),'status','OFF')
                    index += 1
    
def process_data():
    data_temp = []
    while True:
        if read_buffer.qsize() > 0 :
            data = read_buffer.get();
            if data is None:
                break

            if data == 'f7':
                data_temp = []
            elif data == 'aa':
                data_temp.append(data)
                process_data_to_mqtt(data_temp)
                print(data_temp)

            data_temp.append(data)                
        time.sleep(0.01)
    

if __name__ == "__main__":
    socket_client = connect_server()
    mqtt_client = connect_mqtt()

    polling_data()

    read_thread = threading.Thread(target=read_data, args=(), daemon = True)
    read_thread.start()

    process_thread = threading.Thread(target=process_data, args=(), daemon = True)
    process_thread.start()

    read_thread.join()
    process_thread.join()


