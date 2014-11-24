#!/usr/bin/python

import threading
import http.server
import socketserver
import ultraduo

PORT_NUMBER = 8000


def color(string, color):
    ret = '<font style=\"BACKGROUND-COLOR: " + color + "\"><b>'
    ret += string
    ret += '</b></font>'

def error(string, condition):
    if (condition):
        return color(string,'red')
    return ret

def make(channel):
    s = "<hr>\n<table>"
    s = s + "<tr><td><b>Battery:</b></td><td>" + str(channel.battery)  + " (" + str(channel.chargecount) + " cycles)</td></tr>\n"
    s = s + "<tr><td><b>InputVoltage:</b></td><td>" + str(channel.inputvoltage) + " mV</td></tr>\n"
    s = s + "<tr><td><b>Voltage:</b></td><td>" + str(float(channel.voltage)/1000.0) + " mV</td></tr>\n"
    stat = channel.decode_status()
    if (stat == 'ready'):
        stat = color(stat, 'green')
    elif ((stat == 'charging') or (stat == 'discharging') or (stat = 'balancing')):
        stat = color(stat, 'yellow')
    else:
        stat = color(stat, 'red')
    s = s + "<tr><td><b>Status:</b></td><td>" + channel.status + " [<b>" + stat + "</b>]</td></tr>\n"
    s = s + "<tr><td><b>Current:</b></td><td>" + str(channel.current) + " mA</td></tr>\n"
    s = s + "<tr><td><b>Capacity:</b></td><td>" + str(channel.capacity) + " mAh</td></tr>\n"
    s = s + "<tr><td><b>Temperature:</b></td><td>" + error(str(float(channel.temperature)/10.0),channel.temperature > 300) + " degrees C</td></tr>\n"
    s = s + "<tr><td><b>Unknown:</b></td><td>" + str(channel.v2) + " </td></tr>\n"
    s = s + "<tr><td><b>Cells:</b></td><td>"
    for i in range(0,7):
        s = s + str(channel.cells[i]) + ","
    s = s + "</td></tr></table>\n"
    return s

# This class will handle any incoming request from
# a browser 
class myHandler(http.server.BaseHTTPRequestHandler):
    lock = threading.Lock()

    # Handler for the GET requests
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        print   ('Get request received')
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        self.lock.acquire()
        u = ultraduo.ultraduo
        try:
            title = "Graupner Ultra Duo Plus 60"
            s = "<html><head><title>" +title+ "</title><meta http-equiv=\"refresh\" content=\"1\" /></head>"
            s = s + "<body><h1>" +title+ "</h1>"
            s = s + make(u.ch1)
            s = s + make(u.ch2)
            s = s + "<hr></body></html>"
        finally:
            self.lock.release()
        self.wfile.write(bytes(s, "utf-8"))


def start_webserver():
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        server = http.server.HTTPServer(('', PORT_NUMBER), myHandler)
        print ('Started httpserver on port ' , PORT_NUMBER)

        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()



if __name__ == '__main__':
    start_webserver()
