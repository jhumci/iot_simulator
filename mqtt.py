#%%
#!pip install paho-mqtt

# %%
import time
import paho.mqtt.client as paho
import mqtt_credentials
import logging

logging.basicConfig(filename='example.log',  level=logging.INFO)


class MqttClientHandler():
    def __init__(self,client_id,broker, port):
        print(client_id)

        self.client = paho.Client(paho.CallbackAPIVersion.VERSION2)
        
        # enable TLS for secure connection
        #self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set(mqtt_credentials.MQTT_USER, mqtt_credentials.MQTT_PASSWORD)

        self.client.on_connect = self.on_connect
        #self.client.on_disconnect = self.on_disconnect
        #self.client.on_publish = self.on_publish


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
        
        timeout = time.time() + 10   # 10 seconds from now
        while not self.client.is_connected():
            if time.time() > timeout:
                raise Exception("Could not connect to the broker")
            time.sleep(0.2)
        
        return self.client



    def on_disconnect(self, client, userdata, rc):

        client.connected_flag = False
        client.disconnect_flag = True

        # try to reconnect after disconnection
        self.client = self.connect_to_broker(self.broker, self.port)

        logging.warn("MQTT Disconnected") 

    '''
    #works
    def on_publish(self,client, userdata, msgID):
        print("published")
    '''

    def publish_payload(self, topic, payload):
        self.client.publish(topic, payload=payload, qos=1)

    # BUG: I dont know why I ahve to add those properties, did not find them in the docs
    def on_connect(self, client, userdata, flags, rc, properties):
        #print(type(client))
        if rc==0:
            print("connected OK Returned code=",rc)
            client.connected_flag = True  # set flag
            logging.info("MQTT Connected") 
        else:
            print("Bad connection Returned code=",rc)
            client.bad_connection_flag = True
            logging.warn("MQTT Connection failed!") 