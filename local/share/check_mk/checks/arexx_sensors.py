#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import time

def inventory_arexx_sensors(info, req_sensor_type):
    localtime = int(time.time())
    for sensorid,value,stime,signallevel,sensor_type,name in info:
        if sensor_type == req_sensor_type and localtime-saveint(stime) < 900:
            yield "%s %s" % (sensorid,name), None

def check_arexx_sensors(item, params, info, sensor_type):
    localtime = int(time.time())
    sensorid = item.split(' ')[0]
    for line in info:
        if line[0] == sensorid and line[4] == sensor_type and localtime-saveint(line[2]) < 300:
            value=line[1].split(" ")[0]
            return value, line[5], sensorid
    return None,None,None

def check_arexx_sensors_temp(item, params, info):
    value,description,sensorid=check_arexx_sensors(item, params, info,"Temperature")
    if not value == None:
        return check_temperature(savefloat(value),params, "arexx_temp_%s" % sensorid)
    
def check_arexx_sensors_humidity(item, params, info):
    value,description,sensorid=check_arexx_sensors(item, params, info,"Relative Humidity")
    if not value == None:
        return check_humidity(savefloat(value),params)
    

# check declaration
check_info["arexx_sensors.temp"] = {
    "service_description"     : "Temperature %s",
    "check_function"          : check_arexx_sensors_temp,
    "inventory_function"      : lambda info: inventory_arexx_sensors(info,'Temperature'),
    'has_perfdata'            : True,
    "group"                   : "temperature",
    "includes"                : [ "temperature.include" ],
}

check_info["arexx_sensors.humidity"] = {
    "service_description"     : "Humidity %s",
    "check_function"          : check_arexx_sensors_humidity,
    "inventory_function"      : lambda info: inventory_arexx_sensors(info,'Relative Humidity'),
    'has_perfdata'            : True,
    "group"                   : "humidity",
    "includes"                : [ "humidity.include" ],
}
