import output
import datetime

from airPiModels import *

# Time: 2015-08-14 08:31:04.336307
# Temperature: 37.1 C
# Pressure: 959.47 hPa
# Relative_Humidity: 30.0 %
# Light_Level: 417.515274949 Ohms
# Nitrogen_Dioxide: 13790.6976744 Ohms
# Carbon_Monoxide: 127333.333333 Ohms
# Volume: 716.129032258 mV

dType = { 'Time' : 'datetime',
          'Temperature' : 'float',
          'Pressure' : 'float', 
          'Relative_Humidity' : 'float', 
          'Light_Level' : 'float', 
          'Nitrogen_Dioxide' : 'float', 
          'Carbon_Monoxide' : 'float', 
          'Volume' : 'float', 
         }

dTypeList = [ 'Time', 'Temperature', 'Pressure', 'Relative_Humidity', 'Light_Level', 'Nitrogen_Dioxide', 'Carbon_Monoxide', 'Volume', ]

class PGWriter(output.Output):

    # requiredData = ["dbName"]
    optionalData = ["dbName"]
    optionalData = ["tableName"]
    def __init__(self,data):
       self.dbName='airpi'
       if data.has_key('dbName'): self.tableName = data['dbName']
       self.tableName = 'airpidata'
       if data.has_key('tableName'): self.tableName = data['tableName']

    def outputData(self,dataPoints):

        # print "datapoints:", str(dataPoints)

        # we need the data sorted by the keys of dTypeList
        map = { "Time" : datetime.datetime.now() }
        for i in dataPoints:
           map[ i['name'] ] = i["avg"]

        # check if we got everything, otherwise add dummy values
        for k in dTypeList:
            if map.has_key(k): continue
            print "no item found for %s in datapoints" % k
            map[k] = -9999.

        try:
            sess = session()
            apd = AirPiData(temp = map['Temperature'], 
                            pres = map['Pressure'], 
                            relH = map['Relative_Humidity'], 
                            light = map['Light_Level'], 
                            no2 = map['Nitrogen_Dioxide'], 
                            co = map['Carbon_Monoxide'], 
                            vol = map['Volume'], 
                            )
            sess.add(apd)
            sess.commit()
        except Exception, e:
            print "ERROR when uploading to Postgres DB: ", str(e)
            return


