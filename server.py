from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import RPi.GPIO as GPIO
import dht11
from datetime import datetime

serverPort = 8001
sensorPin = 18
tempOffset = -2
humidityOffset = 0
updateIntervalS = 10

dhtClientInstance = None
currentReadings = None

def update_readings():
    global currentReadings
    
    if currentReadings is not None:
        currentTimeStamp = datetime.timestamp(datetime.now())
        readTimeStamp = datetime.timestamp(currentReadings.get('readAt'))
        if readTimeStamp + updateIntervalS > currentTimeStamp:
            return
        
    res = dhtClientInstance.read()
    if not res.is_valid():
        print("got invalid reading from sensor")
        currentReadings = None
        return

    currentReadings = {
        "tempC" : res.temperature + tempOffset,
        "humidity": .01 * res.humidity + humidityOffset,
        "readAt": datetime.now()
    }

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        update_readings()

        if currentReadings is None:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            return
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({
            "tempC": currentReadings.get("tempC"),
            "humidity": currentReadings.get("humidity"),
            "readAt": currentReadings.get("readAt").isoformat(),
        }), "utf-8"))

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    
    dhtClientInstance = dht11.DHT11(pin = sensorPin)
    webServer = HTTPServer(("0.0.0.0", serverPort), MyServer)

    print("Server started on port %s" % (serverPort))
    webServer.serve_forever()
