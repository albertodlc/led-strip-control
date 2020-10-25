import sys, os

lib_path = os.path.realpath(".") + "/modules"
sys.path.append(lib_path)

import flask
from flask import request
import ledStrip as ls
import threading
import time


MAC_ADDR = [
            "85:58:1B:08:AD:ED", # Mesa 1
            "85:58:1B:08:97:4D", # Mesa 2
            "85:58:1B:08:C6:67", # Mesa 3
            "52:14:00:00:C6:A9" # Techo
            ]

# Flask Web App definition
app = flask.Flask(__name__)
app.config["DEBUG"] = False

    
class API():
    @app.route('/led/all/on', methods=['POST'])
    def turn_on_all():
        for m in MAC_ADDR:
            time.sleep(0.5)
            dc = ls.DeviceControl(m)
            dc.turn_on()
            dc.close_connection()
        return ""

    @app.route('/led/all/off', methods=['POST'])
    def turn_off_all():
        for m in MAC_ADDR:
            time.sleep(0.1)
            dc = ls.DeviceControl(m)
            dc.turn_off()
            dc.close_connection()
            
        return ""

app.run(host='0.0.0.0')


