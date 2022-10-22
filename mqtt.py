#%%
#!pip install paho-mqtt

# %%
import time
import paho.mqtt.client as paho
from paho import mqtt


MQTT_BROKER = 'd0b3cc94d52d409a920e09f9cb9f7050.s1.eu.hivemq.cloud' # eg. choosen-name-xxxx.cedalo.cloud
MQTT_PORT = 8883



#%% Testing

"""
# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("123456!pass", "123456!pass")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(broker, port)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("encyclopedia/#", qos=1)

# a single publish, this can also be done in loops, etc.
client.publish("encyclopedia/temperature", payload="hot", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()

"""
# %%


class MqttClient(object):
    def __init__(self,client_id,broker, port):
        self.client = paho.Client(client_id=client_id, userdata=None, protocol=paho.MQTTv5)
        
        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set("123456!pass", "123456!pass")
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect(broker, port)

        # a single publish, this can also be done in loops, etc.
        #client.publish(topic, payload="hot", qos=1)

        #self.client.loop_forever()

    def publish_payload(self, topic, payload):
        self.client.publish(topic, payload=payload, qos=1)

# %%

mqtt_client = MqttClient("IoT-Simulator",MQTT_BROKER, MQTT_PORT)

# %%
mqtt_client.publish_payload("test", """{{"so":"what"}}""")
# %%
