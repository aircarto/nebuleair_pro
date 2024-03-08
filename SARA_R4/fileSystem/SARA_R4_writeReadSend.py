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

def read_serial_lines(ser):
    response_lines = []
    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            break 
        response_lines.append(line)
    return response_lines

ser.write(b'AT+UDELFILE="sensordata2.json"\r')
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'AT+UDWNFILE="sensordata2.json",19\r')            #create the file inside the modem and open the prompt
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'{"temperature": 25}\r')                         #data to write inside the prompt
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'AT+URDFILE="sensordata2.json"\r')                 #read file
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'AT+UHTTP=0,1,"webhook.site"\r')            #Set the URL
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'AT+UHTTPC=0,4,"/b611c895-6639-456d-9bac-cb1a9e429632","data.txt","sensordata2.json",4\r')                  #send the command                                                                                
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

ser.write(b'AT+URDFILE="data.txt"\r')                  #read the reply                                                                                
response_lines = read_serial_lines(ser)
for line in response_lines:
    print(line)

