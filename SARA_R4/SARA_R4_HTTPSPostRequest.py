'''
Script to send data with the SARA-R410 
HTTP POST REQUEST
'''

import serial
import time

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200, #115200 ou 9600
    parity=serial.PARITY_NONE, #PARITY_NONE, PARITY_EVEN or PARITY_ODD
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)

#ser.write(b'AT+UHTTP=0,1,"webhook.site"\r')            #Set the URL
ser.write(b'AT+UHTTPC=0,4,"/b611c895-6639-456d-9bac-cb1a9e429632","data.txt","sensordata.json",4\r')                  #send the command                                                                                
#ser.write(b'AT+URDFILE="data.txt"\r')                  #read the reply                                                                                


response_lines = []

try:
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

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    if ser.is_open:
        ser.close()
        print("Serial closed")