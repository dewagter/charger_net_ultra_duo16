import http.client
import ultraduo
import threading
import time
import settings

def make_request(bat):
    req = "/charger.php"
    req += "?id=CDW" + str(bat)
    req += "&status=charging"
    req += "&voltage=12550"
    req += "&current=2540"
    req += "&temperature=216"
    req += "&volt_cell_1=4123"
    req += "&volt_cell_2=4121"
    req += "&volt_cell_3=4125"
    req += "&volt_cell_4=0"
    req += "&volt_cell_5=0"
    req += "&volt_cell_6=0"
    req += "&volt_cell_7=0"
    req += "&volt_cell_8=0"
    return req
    

def upload_thread():

    while True:

        req = make_request(5)
        print(req)
        conn = http.client.HTTPConnection(settings.MY_PRIVATE_SERVER, 80,timeout=10)
        conn.request("GET", req)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        req = make_request(10)
        print(req)
        conn = http.client.HTTPConnection('log.mavlab.info', 80,timeout=10)
        conn.request("GET", req)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)

        time.sleep(5)

        

if __name__ == '__main__':
    upload_thread()
