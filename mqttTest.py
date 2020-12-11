import paho.mqtt.client as mqtt

broker = 'scumaker.org'
port = 1883
clientId = 'WLED-03bc4a'
DeviceTopic = 'wled/03bc4a'
GroupTopic = 'wled/all'
keeplive = 60


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def run(msg_send):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, keeplive)
    client.publish(DeviceTopic+'/api', payload=msg_send, qos=0)
    client.loop_start()
