# %%

from mqtt import MqttClientHandler
import mqtt_credentials

# %%

mqtt_client_handler = MqttClientHandler("IoT-Simulator",mqtt_credentials.MQTT_BROKER, mqtt_credentials.MQTT_PORT)

# %%

mqtt_client_handler.publish_payload( topic = "Test", payload ="test")
# %%
