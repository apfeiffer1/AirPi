import output
import datetime
import sqlite3

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

class DBWriter(output.Output):

    requiredData = ["dbName"]
    optionalData = ["tableName"]
    def __init__(self,data):
       self.dbName=data["dbName"]
       self.tableName = 'airPiData'
       if data.has_key('tableName'): self.tableName = data['tableName']

       try:
	   dataTypeString = ''
	   for k in dTypeList: 
	       dataTypeString += k +' '+ dType[k]+','

           conn = sqlite3.connect( self.dbName )
           c = conn.cursor()
           # Create table, if it does not yet exist:
           qry = '''CREATE TABLE if not exists %s (%s)''' % (self.tableName, dataTypeString[:-1])
           # print "Query: ", qry
           c.execute( qry )
           c.close()
           conn.close()
       except Exception, e:
          print str(e)
          return False

    def outputData(self,dataPoints):

        # we need the data sorted by the keys of dTypeList
        map = { "Time" : datetime.datetime.now() }
        for i in dataPoints:
           map[ i['name'] ] = i["avg"]
        try:
           conn = sqlite3.connect( self.dbName )
           c = conn.cursor()

           # Insert the data
           arr = []
           for k in dTypeList:
               arr.append( map[k] )
           qry = "INSERT INTO %s VALUES (?,?,?,?,?,?,?,?);" % (self.tableName,)
           # print "Query: ", qry, ' values: ', arr
           c.execute( qry, arr )

           conn.commit()
           conn.close()
            
        except Exception, e:
           print "ERROR when uploading to DB, got exception:", str(e)
           return False
        return True
