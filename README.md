# speedtestmqttjson

Simple Python script to send results of speedtest-cli over MQTT in JSON format

## Description

This program uses [paho-mqtt](https://pypi.org/project/paho-mqtt/), [speedtest-cli](https://pypi.org/project/speedtest-cli/), [geopy](https://pypi.org/project/geopy/), [datetime](https://docs.python.org/3/library/datetime.html#), and [schedule](https://pypi.org/project/schedule/) to:

1. Perform a speedtest using `speedtest-cli`.
2. Log the time that the speedtest was last run with `datetime`.
3. Calculate the distance from the host computer and the server used during the `speedtest-cli` call.
4. Take all of that data, turn it in to JSON, and publish it via MQTT.

 Currently the script is set to perform a speed test every 6 hours but can be changed by modifiying `schedule.every` to whatever you want (reference the schedule docs for more info).

```python
 schedule.every(6).hours.do(job)
 ```

The json data sent via MQTT is structured as follows:

```json
{
   "upload": "upload speed (Mb/s)",
   "download": "download speed (Mb/s)",
   "location": "server location",
   "ping": "ping",
   "distance": "distance between server and host (miles)",
   "time": "timestamp of last speed test (MM-DD-YYYY HH:MM:SS) "
}
```

## Getting Started

You should create a file called `config.py` to store mqtt broker and payload information.

example config.py

```python
mqtt_broker_address="http://broker-address"
mqtt_port=1882
mqtt_user="username"
mqtt_pass="password"
mqtt_topic="topic/foo/bar"
```

## Requirements

Required packages can be found in `requirements.txt`