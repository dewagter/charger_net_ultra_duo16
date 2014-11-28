#!/usr/bin/python

import http.client
import threading
import time
import settings

response = 0

def make_request(channel):
    req = "/charger.php"
    req += "?id=" + channel.battery
    #req += "&time="
    req += "&status=" + channel.status     # discharging, charging en ready
    req += "&voltage=" +str(channel.voltage)
    req += "&current=" + str(channel.current)
    req += "&temperature="+ str(channel.temperature)
    for i in range(0,7):
        req += "&volt_cell_" + str(i+1) + "=" + str(channel.cells[i])
    return req


def upload_server(mycharger):
    lock = threading.Lock()
    while True:
        req = []
        lock.acquire()
        try:
            for ch in mycharger.channels:
                # if battery is connected
                if ((ch.identification == 'identified') and (ch.connection == 'connected')):
                    req.append( make_request(ch) )
        finally:
            lock.release()

        for r in req:
            try:
                print(r)
                conn = http.client.HTTPConnection(settings.LOGSERVER_URL, 80,timeout=10)
                conn.request("GET", r)
                r1 = conn.getresponse()
                response = r1.status
                print(settings.LOGSERVER_URL, r1.status, r1.reason, response)
            except:
                response = -1
                print("Upload failed")

        time.sleep(settings.LOGSERVER_SLEEP)
