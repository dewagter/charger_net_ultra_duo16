#!/usr/bin/python
import _thread

class Channel():
    """Store the charging state of a single battery"""
    def __init__(self):
        # Global status
        self.connected = False
        self.battery = None

        # Basic information
        self.chargetime = 0
        self.status = 'unknown'
        self.voltage = 0
        self.current = 0
        self.cells = [0, 0, 0, 0, 0, 0, 0, 0]

    def identify(self, battery):
        if self.connected and self.battery == None:
            self.battery = battery
            return True
        else:
            return False
    

class Charger():
    def __init__(self):
        self.channels = []
        self.name = 'Generic Charger'

    def identify(self, battery):
        for channel in self.channels:
            if channel.identify(battery):
                return True
        return False

    def start(self):
        _thread.start_new_thread(self.run, ())
