import http.client
import ultraduo
import threading
import time
import settings

def make_request(channel):
    req = "/charger.php"
    req += "?id=CDW" + str(channel.battery)
    req += "&status=" + channel.decode_status()
    # discharging, charging en ready
    req += "&voltage=" +str(channel.voltage)
    req += "&current=" + str(channel.current)
    req += "&temperature="+ str(channel.temperature)
    for i in range(0,7):
        req += "&volt_cell_" + str(i+1) + "=" + str(channel.cells[i])
    return req
    

def upload_thread():
    lock = threading.Lock()
    while True:
        req1 = ''
        req2 = ''
        lock.acquire()
        try:
            u = ultraduo.ultraduo
            req1 = make_request(u.ch1)
            req2 = make_request(u.ch2)
        finally:
            lock.release()

        try:
            print(req1)
            conn = http.client.HTTPConnection(settings.MY_PRIVATE_SERVER, 80,timeout=10)
            conn.request("GET", req1)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            print(req2)
            conn = http.client.HTTPConnection('log.mavlab.info', 80,timeout=10)
            conn.request("GET", req2)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
        except:
            print("Upload failed")    

        time.sleep(5)

        

if __name__ == '__main__':
    upload_thread()
