import serial
import requests
import urllib.request
import json

#baseURL = 'http://api.thingspeak.com/update?api_key=BYNDBXCR7E0W054O&field1='

ser = serial.Serial(
    port='COM7',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
    
# print(ser.name)
seq = []
count = 1
Device_ID = -999

while True:
    for c in ser.read():
        seq.append(chr(c))
        joined_seq = ''.join(str(v) for v in seq)
        if chr(c) == '\n':
#          print("Line " + str(count) + ': ' + joined_seq)
           seq = []
           count += 1
           mydata = joined_seq.split(',')
#           print(mydata)
#           print(len(mydata))
           if len(mydata) >=10:
               t = float(mydata[9])
               h = float(mydata[8])
               pm10 = int(mydata[7])
               pm25 = int(mydata[6])
               pm1 = int(mydata[5])
               Device_ID = mydata[0]
                   
               print(Device_ID)
               print(mydata[1])
               print(mydata[2])
               print(t)
               print(h)
               print(pm10)
               print(pm25)
               print(pm1)

               payload = {
                   'deviceID': Device_ID,
                   'name' : Device_ID,
                   'temp' : str(t),
                   'humidity' : str(h),
                   'pm10': str(pm10),
                   'pm25': str(pm25),
                   'pm1' : str(pm1),
                   'location' : {
                        'lat' : float(mydata[3]),
                        'long': float(mydata[4]),
                       },
                   'now' : {
                        'time' : mydata[2],
                        'date' : mydata[1],
                       }

               }

               headers = {
                    'Token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJ1c2VyIjoiSnVzdGluIEJhayJ9.PSPzrYbIQ4Nb9pHHuew4wZAumGjzibs-tJCjZt25jjk',
                    'Content-Type': 'application/json'
               }
               resp = requests.post('http://butteair.com/data', data=json.dumps(payload), headers=headers)

               print(resp.status_code)
               
               #f = urllib.request.urlopen(baseURL + mydata[9])
               #f = urllib.request.urlopen(baseURL + str(Device_ID) + '&field2=' + mydata[9] + '&field3=' + mydata[8] + '&field4=' + mydata[7] + '&field5=' + mydata[6]+ '&field6=' + mydata[5])
               # https://api.thingspeak.com/update?api_key=writeAPIkey&field1=" + String(temperature)+"&field2=" +String(humidity)
               #f.read()
               #f.close()               

           break
   
ser.close


