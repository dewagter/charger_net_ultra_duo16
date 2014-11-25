#!/usr/bin/python

import threading
import http.server
import socketserver

import beep

PORT_NUMBER = 8000


def color(string, color):
    ret = '<font style=\"BACKGROUND-COLOR: ' + color + '\"><b>'
    ret += string
    ret += '</b></font>'
    return ret

def error(string, condition):
    if (condition):
        return color(string,'red')
    return string

def make(channel, haserror):
    s = "<hr>\n<table>"
    s = s + "<tr><td><b>Battery:</b></td><td>" + str(channel.battery)  + " (" + str(channel.chargecount) + " cycles)</td></tr>\n"
    s = s + "<tr><td><b>InputVoltage:</b></td><td>" + str(float(channel.inputvoltage)/1000.0) + " V</td></tr>\n"
    s = s + "<tr><td><b>Voltage:</b></td><td>" + str(float(channel.voltage)/1000.0) + " V</td></tr>\n"
    stat = channel.status
    if (stat == 'ready'):
        stat = color(stat, 'green')
        # haserror[0] = 1
    elif ((stat == 'charging') or (stat == 'discharging') or (stat == 'balancing')):
        stat = color(stat, 'yellow')
    else:
        stat = color(stat, 'red')
        haserror[0] = 1
    s = s + "<tr><td><b>Status:</b></td><td><b>" + stat + "</b></td></tr>\n"
    s = s + "<tr><td><b>Current:</b></td><td>" + str(channel.current) + " mA</td></tr>\n"
    s = s + "<tr><td><b>Capacity:</b></td><td>" + str(channel.capacity) + " mAh</td></tr>\n"
    s = s + "<tr><td><b>Temperature:</b></td><td>" + error(str(float(channel.temperature)/10.0),channel.temperature > 300) + " degrees C</td></tr>\n"
    s = s + "<tr><td><b>Extra:</b></td><td>" + str(channel.extra) + " </td></tr>\n"
    s = s + "<tr><td><b>Cells:</b></td><td>"
    for i in range(0,8):
        s = s + str(float(channel.cells[i])/1000.0) + "V, "
    s = s + "</td></tr></table>\n"
    return s

# This class will handle any incoming request from
# a browser 
class myHandler(http.server.BaseHTTPRequestHandler):
    #def __init__( self ):
    lock = threading.Lock()
    charger = []

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
        u = self.charger
        try:
            # First make body and check for errors
            haserror = [ 0 ]
            s = "<body>\n<h1>" + u.name + "</h1>\n"
            for c in u.channels:
                s += make(c, haserror)
            s += "<hr>\n</body>\n</html>"

            # Then add header with sound if error
            h = "<html>\n\t<head>\n\t\t<title>" + u.name + "</title>\n"
            h += "\t\t<meta http-equiv=\"refresh\" content=\"1\" />\n"
            if (haserror[0] == 1):
                h += beep.beep()
            h += "\t</head>\n"
            s = h + s
            
        finally:
            self.lock.release()
        self.wfile.write(bytes(s, "utf-8"))


def start_webserver(mycharger):
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        charge_handler = myHandler
        charge_handler.charger = mycharger
        server = http.server.HTTPServer(('', PORT_NUMBER), charge_handler)
        print ('Started httpserver on port ' , PORT_NUMBER)

        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()


import ultraduo
import imaxb6
import charger

if __name__ == '__main__':
    #start_webserver(ultraduo.UltraDuo())
    #start_webserver(imaxb6.ImaxB6())
    c = charger.Charger()
    c.channels.append(charger.Channel())
    c.channels.append(charger.Channel())
    c.channels.append(charger.Channel())
    c.channels.append(charger.Channel())
    start_webserver(c)
