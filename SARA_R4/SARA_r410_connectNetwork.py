'''
Script to connect to the networks we want with the SARA-R410
SFR: 20810
Orange: 20801
'''

import serial
import time

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200, #115200 ou 9600
    parity=serial.PARITY_NONE, #PARITY_NONE, PARITY_EVEN or PARITY_ODD
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 90
)

ser.write(b'AT+COPS?\r')     #searching for available networks (ATTENTION: need at least 1,30 min to respond)

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