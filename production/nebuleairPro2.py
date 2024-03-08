'''

Need to install python3 and other libraries:
sudo apt install python3-pip
sudo pip3 install pyserial --break-system-packages
sudo pip3 install requests --break-system-packages
sudo pip3 install colorama --break-system-packages
'''

import serial
import time
import json

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200, #115200 ou 9600
    parity=serial.PARITY_NONE, #PARITY_NONE, PARITY_EVEN or PARITY_ODD
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 1
)

ser_NPM2 = serial.Serial(
    port='/dev/ttyUSB1',
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

ser_NPM2.write(b'\x81\x12\x6D')
byte_data = ser_NPM2.readline()
stateByte = int.from_bytes(byte_data[2:3], byteorder='big')
Statebits = [int(bit) for bit in bin(stateByte)[2:].zfill(8)]
PM1 = int.from_bytes(byte_data[9:11], byteorder='big')/10
PM25 = int.from_bytes(byte_data[11:13], byteorder='big')/10
PM10 = int.from_bytes(byte_data[13:15], byteorder='big')/10
#create JSON
data = {
    'capteurID': 'nebuleairpro1',
    'sondeID':'NPM2',
    'PM1': PM1,
    'PM25': PM25,
    'PM10': PM10,
    'error_num' : str(Statebits[0])+str(Statebits[1])+str(Statebits[2])
}
json_data = json.dumps(data)
print(json_data)
JSON_lengh = len(json_data)
print("JSON lenght:" + str(JSON_lengh) )

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

