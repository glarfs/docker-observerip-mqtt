#!/usr/bin/env python2.7
from __future__ import with_statement
from lxml import html
import math, time, syslog, requests
import paho.mqtt.client as paho 
import paho.mqtt.publish as publish
import os
import time
#import mosquitto 

broker=os.getenv('OBSERVER_MQTT_HOST', '192.168.1.1')
port=os.getenv('OBSERVER_MQTT_PORT','1883')
entrypoint=os.getenv('OBSERVER_MQTT_ENTRYPOINT',"/test/meteo")
clientID=os.getenv('OBSERVER_MQTT_CLIENTID','observer')
observerIP=os.getenv('OBSERVER_HOST','192.168.1.10')
observerWait=float(os.getenv('OBSERVER_SLEEP','10'))

print("initial configuration:")
#print("mqtt %s:%s%s" % [ broker, port, entrypoint])

#client = mosquitto.Mosquitto("observer")
client = paho.Client(clientID)
c = True
while c: 
  c = False
  url="http://%s/livedata.htm"% observerIP
  try:
    page = requests.get(url)
    tree = html.fromstring(page.content)
    print("Connected from: '%s'" % url)
  except Exception as e:
    print("ObserverIP driver couldn't access the livedata.htm webpage: '%s'" % url)
    print("Error caught was: %s" % e)
    raise
  
  # Can weewx take this value?
  uvi = tree.xpath('//input[@name="uvi"]')[0].value
  inBattery = tree.xpath('//select[@name="inBattSta"]/option')[0].text
  outBattery = tree.xpath('//select[@name="outBattSta"]/option')[0].text
  inTemp = tree.xpath('//input[@name="inTemp"]')[0].value
  inHumid = tree.xpath('//input[@name="inHumi"]')[0].value
  outTemp = tree.xpath('//input[@name="outTemp"]')[0].value
  outHumid = tree.xpath('//input[@name="outHumi"]')[0].value
  absPressure = tree.xpath('//input[@name="AbsPress"]')[0].value
  relPressure = tree.xpath('//input[@name="RelPress"]')[0].value
  windDir = tree.xpath('//input[@name="windir"]')[0].value
  windSpeed = tree.xpath('//input[@name="avgwind"]')[0].value
  windGust = tree.xpath('//input[@name="gustspeed"]')[0].value
  solarRadiation = tree.xpath('//input[@name="solarrad"]')[0].value
  uv = tree.xpath('//input[@name="uv"]')[0].value
  hourlyRain = tree.xpath('//input[@name="rainofhourly"]')[0].value
  dailyRainAccum = tree.xpath('//input[@name="rainofdaily"]')[0].value
  print inBattery, outBattery, uvi, inTemp, inHumid, outTemp, outHumid, absPressure, relPressure, windDir, windSpeed, windGust, solarRadiation, uv, dailyRainAccum
  try:
    client.connect(broker,port)
    print("mqtt '%s' connected" % broker)
  except Exception as e:
    print("ObserverIP driver couldn't access mqtt server : '%s'" % broker)
    print("Error caught was: %s" % e)
    raise
  client.publish( "{0}/status".format(entrypoint),payload="1")
  client.publish( "{0}/solar/uvi".format(entrypoint),payload=uvi , retain=True)
  client.publish( "{0}/in/battery".format(entrypoint),payload=inBattery, retain=True)
  client.publish( "{0}/out/battery".format(entrypoint),payload=outBattery, retain=True) 
  client.publish( "{0}/in/humid".format(entrypoint),payload=inHumid, retain=True)
  client.publish( "{0}/out/humid".format(entrypoint),payload=outHumid, retain=True)
  client.publish( "{0}/in/temp".format(entrypoint),payload=inTemp, retain=True)
  client.publish( "{0}/out/temp".format(entrypoint),payload=outTemp,retain=True)
  client.publish( "{0}/absPressure".format(entrypoint),payload=absPressure, retain=True)
  client.publish( "{0}/relPressure".format(entrypoint),payload=relPressure, retain=True)
  client.publish( "{0}/wind/dir".format(entrypoint),payload=windDir, retain=True)
  client.publish( "{0}/wind/speed".format(entrypoint),payload=windSpeed, retain=True)
  client.publish( "{0}/wind/gust".format(entrypoint),payload=windGust, retain=True)
  client.publish( "{0}/solar/radiation".format(entrypoint),payload=solarRadiation, retain=True)
  client.publish( "{0}/solar/uv".format(entrypoint),payload=uv, retain=True)
  client.publish( "{0}/rain/houry".format(entrypoint),payload=hourlyRain,retain=True)
  client.publish( "{0}/rain/daily".format(entrypoint),payload=dailyRainAccum,retain=True)
  # WeeWx Mqtt
  client.publish( "{0}/inTemp_C".format(entrypoint),payload=inTemp, retain=True)
  client.publish( "{0}/inHumidity".format(entrypoint),payload=inHumid, retain=True)  
  client.publish( "{0}/outTemp_C".format(entrypoint),payload=outTemp,retain=True)
  client.publish( "{0}/outHumidity".format(entrypoint),payload=outHumid, retain=True)
  client.publish( "{0}/windSpeed_kph".format(entrypoint),payload=windSpeed, retain=True)
  client.publish( "{0}/windDir".format(entrypoint),payload=windDir, retain=True)
  client.publish( "{0}/windGust_kph".format(entrypoint),payload=windGust, retain=True)  
  client.publish( "{0}/radiation_Wpm2".format(entrypoint),payload=solarRadiation, retain=True)
  client.publish( "{0}/UV".format(entrypoint),payload=uv, retain=True)
  client.publish( "{0}/rainRate_cm_per_hour".format(entrypoint),payload=hourlyRain,retain=True)
  client.publish( "{0}/dayRain_cm".format(entrypoint),payload=dailyRainAccum,retain=True)
  client.publish( "{0}/pressure_mbar".format(entrypoint),payload=absPressure, retain=True)
  client.publish( "{0}/altimeter_mbar".format(entrypoint),payload=relPressure, retain=True)
  client.publish( "{0}/illuminance".format(entrypoint),payload=uvi , retain=True)  
  client.publish( "{0}/outBatteryStatus".format(entrypoint),payload=outBattery, retain=True) 
  client.publish( "{0}/inBatteryStatus".format(entrypoint),payload=inBattery, retain=True)
  

  
 
  
  print("mqtt published")
  print("sleep %s" % observerWait)
  # sleep time
  time.sleep(observerWait)
  


#except Exception as e:
#  print("ObserverIP driver couldn't access the livedata.htm webpage.")
#  print("Error caught was: %s" % e)
#  client.publish( "{}/status".format(entrypoint),"0")
#  raise

