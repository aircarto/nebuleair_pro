'''
Script to run every minutes as a cronjob:
* * * * * /usr/bin/python3 /home/nebuleairpro/nextpm/scanUSB.py

Read NextPM values over 3 USB ports and send them to aircarto's server with the SARA R4 modem

Need to install python3 and other libraries:
sudo apt install python3-pip
sudo pip3 install pyserial --break-system-packages
sudo pip3 install requests --break-system-packages
sudo pip3 install colorama --break-system-packages

'''

import serial
import requests
import json
from colorama import Fore, Back, Style


ser_NPM2 = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)

ser_SARA = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200, #115200 ou 9600
    parity=serial.PARITY_NONE, #PARITY_NONE, PARITY_EVEN or PARITY_ODD
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)

print("Getting data from 1st NPM:")
ser_NPM2.write(b'\x81\x12\x6D')      #data60s

byte_data = ser_NPM2.readline()
stateByte = int.from_bytes(byte_data[2:3], byteorder='big')
Statebits = [int(bit) for bit in bin(stateByte)[2:].zfill(8)]
PM1 = int.from_bytes(byte_data[9:11], byteorder='big')/10
PM25 = int.from_bytes(byte_data[11:13], byteorder='big')/10
PM10 = int.from_bytes(byte_data[13:15], byteorder='big')/10
print(f"PM1: {PM1}")
print(f"PM25: {PM25}")
print(f"PM10: {PM10}")
print(f"State: {Statebits}")
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

######### SARA ###########
print("######### SARA ###########")

#First delete the sensordata file
ser_SARA.write(b'AT+UDELFILE="sensordata.json"\r')
response_lines = []
while True:
    line = ser_SARA.readline().decode('utf-8').strip()
    if not line:
        break  # Break the loop if an empty line is encountered
    response_lines.append(line)
for line in response_lines:
    print(Fore.RED + line)

#then creating again the file
ser_SARA.write(b'AT+UDWNFILE="sensordata.json",150\r')
response_lines = []
while True:
    line = ser_SARA.readline().decode('utf-8').strip()
    if not line:
        break  # Break the loop if an empty line is encountered
    response_lines.append(line)
for line in response_lines:
    print(line)

print(Fore.WHITE +"Prompt open:")
json_bytes = (json_data + '\r').encode('utf-8')
ser_SARA.write(json_bytes)

response_lines = []
while True:
    line = ser_SARA.readline().decode('utf-8').strip()
    if not line:
        break  # Break the loop if an empty line is encountered
    response_lines.append(line)
for line in response_lines:
    print(Fore.GREEN + line)

print(Fore.WHITE +"Checking the file")
ser_SARA.write(b'AT+URDFILE="sensordata.json"\r')                 #read file
response_lines = []
while True:
    line = ser_SARA.readline().decode('utf-8').strip()
    if not line:
        break  # Break the loop if an empty line is encountered
    response_lines.append(line)
for line in response_lines:
    print(Fore.YELLOW + line)


#HTTP post request
print(Fore.WHITE +"Sending Now to server:")

ser_SARA.write(b'AT+UHTTPC=0,4,"/b611c895-6639-456d-9bac-cb1a9e429632","data.txt","sensordata.json"\r')                  #send the command                                                                                
response_lines = []
while True:
    line = ser_SARA.readline().decode('utf-8').strip()
    if not line:
        break  # Break the loop if an empty line is encountered
    response_lines.append(line)
for line in response_lines:
    print(Fore.RED +line)