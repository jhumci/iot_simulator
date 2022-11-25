#%%
#!pip install paho-mqtt

# %%
import time
import paho.mqtt.client as paho
from paho import mqtt
import threading
import config
import mqtt_credentials



class MqttClientHandler():
    def __init__(self,client_id,broker, port):
        print(client_id)

        self.client = paho.Client(client_id=client_id, protocol=paho.MQTTv5)
        
        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set(mqtt_credentials.MQTT_USER, mqtt_credentials.MQTT_USER)
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        #self.client.connect(broker, port)
        
        # http://www.steves-internet-guide.com/python-mqtt-client-changes/
        # a single publish, this can also be done in loops, etc.
        #client.publish(topic, payload="hot", qos=1)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish


        self.client = self.connect_to_broker(broker, port)

        # TODO: Make the client reconnect
        # http://www.steves-internet-guide.com/loop-python-mqtt-client/
        #self.client.loop_forever()

        #clientloop_thread = threading.Thread(target=self.connect)
        #clientloop_thread.setDaemon(True)     
        #clientloop_thread.start()
        
    def connect_to_broker(self, broker, port):
        self.client.connect_async(host=broker, port=port, keepalive=120)
        self.client.loop_start()
        
        while not self.client.is_connected(): #TODO for ->fehlermeldung
            time.sleep(0.2)
     
        def on_connect(client, userdata, flags, rc):
            if rc==0:
                print("connected OK Returned code=",rc)
                client.connected_flag = True  # set flag
            else:
                print("Bad connection Returned code=",rc)
                client.bad_connection_flag = True
        
        return self.client   

    def on_disconnect(self, client, userdata, rc):

        client.connected_flag = False
        client.disconnect_flag = True

    def on_publish(self,client, userdata, msgID):
        print("published")

    def publish_payload(self, topic, payload):
        self.client.publish(topic, payload=payload, qos=1)



# %%
