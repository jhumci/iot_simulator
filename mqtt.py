#%%
#!pip install paho-mqtt

# %%
import time
import paho.mqtt.client as paho
from paho import mqtt

import config




class MqttClient(object):
    def __init__(self,client_id,broker, port):
        self.client = paho.Client(client_id=client_id, userdata=None, protocol=paho.MQTTv5)
        
        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set(config.MQTT_USER, config.MQTT_USER)
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect(broker, port)

        # a single publish, this can also be done in loops, etc.
        #client.publish(topic, payload="hot", qos=1)

        # TODO: Make the client reconnect
        # http://www.steves-internet-guide.com/loop-python-mqtt-client/
        #self.client.loop_forever()

        self.client.loop_start()

    def publish_payload(self, topic, payload):
        self.client.publish(topic, payload=payload, qos=1)


# %%

# mqtt_client = MqttClient("IoT-Simulator",MQTT_BROKER, MQTT_PORT)

# %%
# mqtt_client.publish_payload("test", """{{"so":"what"}}""")
# %%
