import random
from paho.mqtt import client as mqtt_client
from threading import Thread

class MqttClient:
    # MQTT General Info
    broker = '34.143.164.218'
    port = 1883
    topic = "python/mqtt"
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    # username = 'emqx'
    # password = 'public'
    def __init__(self, intPrintFunc, extPrintFunc):
        self.intPrintFunc = intPrintFunc
        self.extPrintFunc = extPrintFunc
        self.client = None
        self.isSubcribed = False

    def isConnected(self):
        return self.client != None
    
    def disconnect(self):
        self.client.disconnect()

    def listen(self):
        if not self.isConnected():
            self.extPrintFunc("Cannot perform listening. No client specified!")
            return
        def loop():
            self.client.loop_forever()
        self.subscribe()
        connect = Thread(target=loop, name="mqtt_connect")
        connect.start()

    def connect(self):
        if self.isConnected():
            return
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                self.intPrintFunc("Connected")
            else:
                self.intPrintFunc("Failed to connect")

        self.intPrintFunc("Connecting")
        self.client = mqtt_client.Client(self.client_id)
    #    client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def subscribe(self):
        if self.isSubcribed:
            return
        if not self.isConnected():
            self.connect()
        def on_message(client, userdata, msg):
            self.extPrintFunc(f"[Topic: {msg.topic}]: {msg.payload.decode()}")

        self.client.subscribe(self.topic)
        self.isSubcribed = True
        self.extPrintFunc("Subcribed! Listening ...")
        self.client.on_message = on_message

    def connectAndListen(self):
        if self.isConnected():
            return
        self.connect()
        self.listen()

    def publish(self, msg):
        if not self.isConnected():
            self.intPrintFunc("Cannot perform publishing. No client specified!")
            return
        result = self.client.publish(self.topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            self.intPrintFunc(f"{self.topic}: {msg}")
        else:
            self.intPrintFunc(f"Failed to send message to topic {self.topic}")