'''
Script to read data from one NextPM and send it to the server with the SARA R410 module
Can be lauched as a cronjob every minutes
* * * * * /usr/bin/python3 /home/nebuleairpro/production/nebuleairpro3.py

-> ATTENTION: SARA R4 Module should me turned on first!


Need to install python3 and other libraries:
sudo apt install python3-pip
sudo pip3 install pyserial --break-system-packages
sudo pip3 install requests --break-system-packages
sudo pip3 install colorama --break-system-packages

Send data as a JSON:
{
  "capteurID": "nebuleairpro1",
  "data": [
    {
      "PM1": 0.9,
      "PM25": 1,
      "PM10": 0,
      "error_num": "000"
    },
    {
      "PM1": 1.2,
      "PM25": 1.7,
      "PM10": 5.2,
      "error_num": "000"
    },
    {
      "PM1": 1.4,
      "PM25": 2.4,
      "PM10": 2.4,
      "error_num": "000"
    }
  ]
}

'''

import serial
import time
import json

capteurID = 'nebuleairpro1'

#SARA R4 Module
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200, #115200 ou 9600
    parity=serial.PARITY_NONE, #PARITY_NONE, PARITY_EVEN or PARITY_ODD
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 4
)

#First NPM
ser_NPM1 = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)

#Second NPM
ser_NPM2 = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)

#Third NPM
ser_NPM3 = serial.Serial(
    port='/dev/ttyUSB3',
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)

def read_serial_lines(ser):
    response_lines = []
    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            break 
        response_lines.append(line)
    return response_lines

nextPM_serlist = [ser_NPM1, ser_NPM2, ser_NPM3]
data = {'capteurID' : capteurID , 'data': []}
nextPM_id = 1

for nextPM_ser in nextPM_serlist:

    #Write command to NextPM
    nextPM_ser.write(b'\x81\x12\x6D')     #data60s
    #Read response
    byte_data = nextPM_ser.readline()
    stateByte = int.from_bytes(byte_data[2:3], byteorder='big')
    Statebits = [int(bit) for bit in bin(stateByte)[2:].zfill(8)]
    PM1 = int.from_bytes(byte_data[9:11], byteorder='big')/10
    PM25 = int.from_bytes(byte_data[11:13], byteorder='big')/10
    PM10 = int.from_bytes(byte_data[13:15], byteorder='big')/10
    #create python object
    sensor_data = {
        'sondeID': 'NPM' + str(nextPM_id),
        'PM1': PM1,
        'PM25': PM25,
        'PM10': PM10,
        'err' : str(Statebits[0])+str(Statebits[1])+str(Statebits[2])
    }
    data['data'].append(sensor_data)
    nextPM_id = nextPM_id + 1

json_data = json.dumps(data) #convert python object to JSON
print(json_data)
JSON_lengh = len(json_data)
print("JSON lenght:" + str(JSON_lengh) )

########## SARA AT commands ###############
ser.write(b'AT+UDELFILE="sensordata2.json"\r')              #delete the file
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

commandeCreateFile = ("AT+UDWNFILE=\"sensordata2.json\","+ str(JSON_lengh) + '\r').encode('utf-8')
ser.write(commandeCreateFile)            #create the file inside the modem and open the prompt
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

#ser.write(b'{"temperature": 26}\r')                         #data to write inside the prompt
json_bytes = (json_data + '\r').encode('utf-8')
ser.write(json_bytes)
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'AT+URDFILE="sensordata2.json"\r')                 #read file
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'AT+UHTTP=0,1,"data.nebuleair.fr"\r')            #Set the URL
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'AT+UHTTPC=0,4,"/pro_LTE.php","data.txt","sensordata2.json",4\r')                  #send the command                                                                                
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'AT+URDFILE="data.txt"\r')                  #read the reply                                                                                
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

