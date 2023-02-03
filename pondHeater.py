#!/usr/bin/env python3
import json
import sys
import asyncio
import traceback
from time import time, sleep
from os import environ
import requests
from datetime import date, datetime
from ambient_api.ambientapi import AmbientAPI
from kasa import SmartStrip

def logIt(msg):
    print(str(datetime.now())[0:16] + ":\t" + msg, file=sys.stderr, flush=True)

async def main(): 
    PondTargetTempHigh = 38.0
    PondTargetTempLow = 37.0
    while True:
        try:
            weather = AmbientAPI(AMBIENT_API_KEY="x",AMBIENT_APPLICATION_KEY="x",AMBIENT_ENDPOINT="https://api.ambientweather.net/v1")
            weatherStation = weather.get_devices()[0];
            sleep(1)
            WeatherDataList = weatherStation.get_data()
            weatherData = WeatherDataList[0]
            pondTemp = float(weatherData["temp4f"]);

            #KASA STRIP
            strip = SmartStrip("192.168.1.74")
            await strip.update()  # Request the update
            plug = strip.children[1]

            if plug.is_on and pondTemp > PondTargetTempHigh:
                await plug.turn_off()
                logIt(plug.alias + "\tPOWER=" + str(plug.is_on) + "\tPond Temp=" + str(pondTemp) + "\tTURNING OFF")
            elif not plug.is_on and pondTemp < PondTargetTempLow:
                await plug.turn_on()
                logIt(plug.alias + "\tPOWER=" + str(plug.is_on) + "\tPond Temp=" + str(pondTemp) + "\tTURNING ON")
            else:
                logIt(plug.alias + "\tPOWER=" + str(plug.is_on) + "\tPond Temp=" + str(pondTemp) + "\tNO ACTION")

        except:
           traceback.print_exc()
           sleep(60)
        sleep(600) 

if __name__ == '__main__':
    asyncio.run(main())