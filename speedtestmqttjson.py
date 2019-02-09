import schedule, time
from datetime import datetime
import config
import paho.mqtt.client as mqttClient
from geopy import distance
import speedtest, json, urllib


Connected = False 
broker_address= config.mqtt_broker_address
port=config.mqtt_port
user=config.mqtt_user
password=config.mqtt_pass



def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")


def getSpeed():
    global json_data
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    s.results.share()
    results_dict = s.results.dict()
    upload = round(results_dict["upload"]/1000000,2)
    download = round(results_dict["download"]/1000000,2)
    ping = round(results_dict["ping"],2)
    local_lat = results_dict["client"]["lat"]
    local_lon = results_dict["client"]["lon"]
    server_location = results_dict["server"]["name"]
    server_lat = results_dict["server"]["lat"]
    server_lon = results_dict["server"]["lon"]
    coords1 = "({},{})".format(local_lat,local_lon)
    coords2 = "({},{})".format(server_lat,server_lon)
    dist = round(distance.distance((local_lat,local_lon),(server_lat,server_lon)).miles,2)
    current_time = datetime.now()
    month = current_time.strftime("%m")
    day = current_time.strftime("%d")
    hour = current_time.strftime("%I")
    minute = current_time.strftime("%M")
    second = current_time.strftime("%s")[:2]
    year = current_time.strftime("%Y")
    time_str = "{}-{}-{} {}:{}:{}".format(month,day,year,hour,minute,second)
    json_data = json.dumps({'upload': upload, 'download': download, 'location': server_location, 'ping': ping, 'distance': dist, 'time': time_str})  
    return json_data


getSpeed()

def job():
 getSpeed()


schedule.every(6).hours.do(job)

client = mqttClient.Client("Python")
client.username_pw_set(user, password=password)
client.on_connect= on_connect
client.connect(broker_address, port=port)
client.loop_start()
while Connected != True:    #Wait for connection
    time.sleep(0.1)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
        client.publish(config.mqtt_topic,json_data)
 
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()
 