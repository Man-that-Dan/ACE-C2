# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import requests
import json
import codecs
import requests
import operator
import math 

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def distance(self,lat1, lon1, lat2, lon2):
        p = math.pi/180     #Pi/180

        a = 0.5 - math.cos((lat2 - float(lat1) * p)/2 + math.cos(float(lat1) * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - float(lon1)) * p))) / 2
        return 12742 * math.asin(math.sqrt(a)) #2*R*asin...


    def findClose(self,inLat, inLong):
        dictD = json.loads(codecs.open('gpdmini.json', 'r', 'utf-8-sig').read())
        distanceDict = {}
        # keep array of top N values
        # calculate the distance from each value in array
        # check if distance is less than the top in the array. 
        # if less, then put it in (keep array of index values)

        # THANK SALVADOR DALI ON https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula

        for plant in dictD["global_power_plant_database"]:
            plantDistance = self.distance(inLat,inLong,float(plant["latitude"]),float(plant["longitude"]))
            distanceDict[dictD["global_power_plant_database"].index(plant)] = abs(plantDistance)
            if len(distanceDict) > 3:
                    drop = max(distanceDict,key=distanceDict.get)
                    distanceDict.pop(drop)

        print(distanceDict)
        # These are the three closest. 

        #Now get and format their data        


    # for plant in dictD["global_power_plant_database"]:
    #         print(plant["latitude"])
    #         print(plant["longitude"])

        outfile = {}

        outfile["data"] = [dictD["global_power_plant_database"][int(list(distanceDict.keys())[0])],dictD["global_power_plant_database"][int(list(distanceDict.keys())[1])],dictD["global_power_plant_database"][int(list(distanceDict.keys())[2])]]

        return json.dumps(outfile)



    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        # self.wfile.write(bytes("<body>", "utf-8"))
        # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))
        requestString = self.path

        drrs = (requestString[1:])
        arr = drrs.split(',')
        # print("Doctored string to ",drrs)
        # print(drrs.split(','))
        # print('Will pass in ',drrs.split()[0],drrs.split()[1])
        self.wfile.write(self.findClose(arr[0],arr[1]).encode())




def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'OPTIONS':
        start_response(
        '200 OK',
        [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
            ('Access-Control-Allow-Methods', 'POST'),
        ]
        )
        return ''

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")