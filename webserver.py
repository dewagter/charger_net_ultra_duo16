#!/usr/bin/python

import threading
import http.server
import socketserver
import beep
import _thread

def color(string, color):
    ret = '<font style=\"BACKGROUND-COLOR: ' + color + '\"><b>'
    ret += string
    ret += '</b></font>'
    return ret

def error(string, condition):
    if (condition):
        return color(string,'red')
    return string

def write_channel(channel, haserror):
    s = "<hr /><table>\n"
    if channel.battery != None:
        s += "<tr><td><b>Battery:</b></td><td>" + str(channel.battery.id) + " / " + str(channel.connected) + "</td></tr>\n"
    else:
        s += "<tr><td><b>Battery:</b></td><td> Unknown /" + str(channel.connected) + "</td></tr>\n"
    s += "<tr><td><b>Voltage:</b></td><td>" + str(float(channel.voltage)/1000.0) + " V</td></tr>\n"
    stat = channel.status
    if (stat == 'ready'):
        stat = color(stat, 'green')
        # haserror[0] = 1
    elif ((stat == 'charging') or (stat == 'discharging') or (stat == 'balancing')):
        stat = color(stat, 'yellow')
    else:
        stat = color(stat, 'red')
        haserror[0] = 1
    s += "<tr><td><b>Status:</b></td><td><b>" + stat + "</b></td></tr>\n"
    s += "<tr><td><b>Current:</b></td><td>" + str(channel.current) + " mA</td></tr>\n"
    #s += "<tr><td><b>Capacity:</b></td><td>" + str(channel.capacity) + " mAh</td></tr>\n"
    #s += "<tr><td><b>Temperature:</b></td><td>" + error(str(float(channel.temperature)/10.0),channel.temperature > 300) + " degrees C</td></tr>\n"
    s += "<tr><td><b>Cells:</b></td><td>"
    for i in range(0,8):
        s += str(float(channel.cells[i])/1000.0) + "V, "
    s += "</td></tr></table>\n"
    return s

# This class will handle any incoming request from
# a browser 
class chargeHandler(http.server.BaseHTTPRequestHandler):
    #def __init__( self ):
    lock = threading.Lock()
    chargers = []

    def log_message(self, format, *args):
        return

    # Handler for the GET requests
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        self.lock.acquire()
        try:
            # First make body and check for errors
            haserror = [ 0 ]
            body = "<body>\n"
            for charger in chargeHandler.chargers:
                body += "<h1>" + charger.name + "</h1>\n"
                for ch in charger.channels:
                    body += write_channel(ch, haserror)
            body += "</body>\n"

            # Then add header with sound if error
            head = "<head>\n\t\t<title>Network Chargers</title>\n"
            head += "\t\t<meta http-equiv=\"refresh\" content=\"1\" />\n"
            if (haserror[0] == 1):
                head += beep.beep()
            head += "\t</head>\n"
            total = "<html>\n" + head + body + "</html>"
            
        finally:
            self.lock.release()
        self.wfile.write(bytes(total, "utf-8"))


def start_webserver(chargers, port):
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        chargeHandler.chargers = chargers
        server = http.server.HTTPServer(('', port), chargeHandler)
        print ('Started httpserver on port ' , port)

        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()

def start(chargers, port = 8000):
    _thread.start_new_thread(start_webserver, (chargers, port))

import settings

if __name__ == '__main__':
    start(settings.chargers)
    while True:
        pass
