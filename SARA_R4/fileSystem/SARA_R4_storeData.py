'''
Script to store data/files inside the SARA-R410
First create the file
Wait for the prompt (>)
Type the data
'''

import serial
import time

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200, #115200 ou 9600
    parity=serial.PARITY_NONE, #PARITY_NONE, PARITY_EVEN or PARITY_ODD
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 1
)

#ser.write(b'ATI\r')                                         #General Information
#ser.write(b'AT+UDWNFILE="sensordata.json",19\r')            #create the file inside the modem and open the prompt
#ser.write(b'{"temperature": 21}\r')                         #data to write inside the prompt
ser.write(b'AT+URDFILE="sensordata.json"\r')                 #read file

response_lines = []

# Read lines until a timeout occurs
response_lines = []
while True:
    line = ser.readline().decode('utf-8').strip()
    if not line:
        break  # Break the loop if an empty line is encountered
    response_lines.append(line)
# Print the response
for line in response_lines:
    print(line)


