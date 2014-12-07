#!/usr/bin/python

import http.client
import threading
import time
import _thread

def make_request(channel):
    req = "/charger.php"
    req += "?id=" + channel.battery.id
    #req += "&time="
    req += "&status=" + channel.status     # discharging, charging en ready
    req += "&voltage=" +str(channel.voltage)
    req += "&current=" + str(channel.current)
    req += "&temperature="+ str(channel.temperature)
    for i in range(0, channel.battery.cells):
        req += "&volt_cell_" + str(i+1) + "=" + str(channel.cells[i])
    return req

def upload_server(chargers, address, timeout):
    lock = threading.Lock()
    while True:
        req = []
        lock.acquire()
        try:
            for charger in chargers:
                for ch in charger.channels:
                    # if battery is connected and identified
                    if ch.battery != None and ch.connected and ch.status != "idle":
                        req.append( make_request(ch) )
        finally:
            print("Upload: Lock Error")
            lock.release()

        for r in req:
            try:
                print(r)
                conn = http.client.HTTPConnection(address, 80,timeout=10)
                conn.request("GET", r)
                r1 = conn.getresponse()
                print(address, r1.status, r1.reason)
            except:
                print("Upload failed")

        time.sleep(timeout)

def start(chargers, address, timeout):
    _thread.start_new_thread(upload_server, (chargers, address, timeout))
