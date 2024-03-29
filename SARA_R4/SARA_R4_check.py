'''
Script to see if the SARA-R410 is running
'''

import serial
import time

ser = serial.Serial(
    port='/dev/ttyS0',  #USB0 or ttyS0
    baudrate=115200, #115200 ou 9600
    parity=serial.PARITY_NONE, #PARITY_NONE, PARITY_EVEN or PARITY_ODD
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)

ser.write(b'ATI\r')            #General Information
#ser.write(b'AT+CCID?\r')       #SIM card number
#ser.write(b'AT+CPIN?\r')       #Check the status of the SIM card
#ser.write(b'AT+CIND?\r')       #Indication state (last number is SIM detection: 0 no SIM detection, 1 SIM detected, 2 not available)
#ser.write(b'AT+UGPIOR=?\r')   #Reads the current value of the specified GPIO pin
#ser.write(b'AT+UGPIOC?\r')     #GPIO select configuration
#ser.write(b'AT+COPS=?\r')     #Check the network and cellular technology the modem is currently using
#ser.write(b'AT+CFUN=?\r')     #Selects/read the level of functionality 
#ser.write(b'AT+URAT=?\r')     #Radio Access Technology 
#ser.write(b'AT+USIMSTAT?')
#ser.write(b'AT+IPR?')           #Check/Define baud rate
#ser.write(b'AT+CMUX=?')



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
