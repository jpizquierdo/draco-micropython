from umqtt.simple import MQTTClient
from draco.config2 import WATERPUMP_TOPIC


class mqttInterface(object):
    def __init__(self):
        self.server: str = ""
        self.port: int = 1883
        self.client: MQTTClient = None
        self.waterPump: bool = False

    def subscribe_callback(self, topic, msg):
        """Received messages from subscriptions will be delivered to this callback"""
        #print((topic, msg))
        if topic.decode() == WATERPUMP_TOPIC:
            self.waterPump = bool(int(msg.decode()))

    def connectMQTT(self, client_id: str, server: str, port: int):
        """Connects to Broker"""
        # Client ID can be anything
        print(f"configuring {client_id} with server {server} and port {port}")
        self.client = MQTTClient(
            client_id=client_id.encode(),
            server=server,
            port=port,
        )
        self.client.set_callback(self.subscribe_callback)
        self.client.connect()

    def subscribe(self, topic: str, qos: int = 0):
        """subscribe to a given topic"""
        print(f"Subscribed to {topic}")
        self.client.subscribe(topic=topic.encode(), qos=qos)

    def publish(self, topic: str, payload: str, retain: bool = True, qos: int = 0):
        """publish the payload to the topic"""
        self.client.publish(
            topic=topic.encode(),
            msg=payload.encode(),
            retain=retain,
            qos=qos,
        )

    def disconnect(self):
        """Disconnects to Broker"""
        print("Disconnecting MQTT client")
        self.client.disconnect()
