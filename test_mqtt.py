# %%

from mqtt import MqttClientHandler
import mqtt_credentials
import time

# %%

mqtt_client_handler = MqttClientHandler("IoT-Simulator",mqtt_credentials.MQTT_BROKER, mqtt_credentials.MQTT_PORT)

# %%

mqtt_client_handler.publish_payload( topic = "Test", payload ="test22")
# %%


counter = 0

while True:
    mqtt_client_handler.publish_payload( topic = "Test", payload =str(counter))
    time.sleep(10)
    counter = counter + 1
# %%
