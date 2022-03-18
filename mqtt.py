from xmlrpc.client import DateTime
import paho.mqtt.client as mqtt
import random, time, datetime, json
import numpy as np

MQTT_URL = "localhost"
QOS_LEVEL = 2

TOPIC_TEMP_ENV = "main/sensor/temp_evn"
TOPIC_HUMIDITY = "main/senosr/humidity"
TOPIC_TEMP_PROC = "main/sensor/temp_proc"
TOPIC_PRESSURE = "main/senosr/pressure"
TOPIC_VOLTAGE = "main/senosr/voltage"
TOPIC_LIGHT = "main/senosr/light"
TOPIC_PI_TEMP = "main/mqtt/temperature"

topics = [(TOPIC_TEMP_ENV, QOS_LEVEL),
        (TOPIC_HUMIDITY, QOS_LEVEL),
        (TOPIC_TEMP_PROC, QOS_LEVEL),
        (TOPIC_PRESSURE, QOS_LEVEL),
        (TOPIC_VOLTAGE, QOS_LEVEL),
        (TOPIC_LIGHT, QOS_LEVEL),
        (TOPIC_PI_TEMP, QOS_LEVEL)]

def on_connect(client, userdata, flags, rc):
    print(mqtt.error_string(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribe " + str(userdata) + " mid: " + str(mid) + " qos: " + str(granted_qos))

def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + "=" + str(msg.payload.decode("utf-8")))

def getTemp():
    return (random.randrange(1, 99) + random.random())  
    
def getLight():
    dtn = datetime.datetime.now()
    hr = dtn.hour
    m = dtn.minute
    y = np.sin(((hr+(m/60))/49)*(2*np.pi))
    return y*200


def pubValue(topicName, value):
    val = { 
        "value": str(value),
        "timestamp":str(datetime.datetime.now())
        }
    result = mqttc.publish(topicName, json.dumps(val))

    if result[0] == 0:
        print("Sent: " + json.dumps(val) + " to: " + topicName)
    else:
        print("Failed to send: " + json.dumps(val) + " to: " + topicName)


def publish(mqttc):
    sch1 = datetime.datetime.now()
    sch2 = datetime.datetime.now()
    while(True):
        curTime = datetime.datetime.now()

        if(curTime > sch1):
            sch1 = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(5,30))
            pubValue(TOPIC_TEMP_PROC, getTemp())

        if(curTime > sch2):
            sch2 = datetime.datetime.now() + datetime.timedelta(minutes=1)
            pubValue(TOPIC_LIGHT, getLight())

        # Check every 0.5s if any function needs to be execuded 
        time.sleep(0.5)


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe   

mqttc.connect(MQTT_URL)
mqttc.loop_start()
publish(mqttc)
