#Send message over serial bus and read reply
import serial
import time
import binascii


print("Start communication")

# ttyUSB1 is for test
# ttyUSB0 is the NextPM
ser = serial.Serial('/dev/ttyUSB1', 115200 , timeout=1) 

try:
    # Send data
    ser.write(b'Hello')
    #ser.write(b'\x81\x11\x6E')      #data10s
    #ser.write(b'\x81\x12\x6D')      #data60s
    #ser.write(b'\x81\x16\x69')      #state

    # Wait for a moment (adjust as needed)
    time.sleep(0.5)

    # Read the response
    #response = ser.readline().decode('utf-8').strip()
    response_hex = ser.read_all()
    #response_ascii = binascii.hexlify(response_hex).decode('utf-8')

    # Print the response
    #print(f'Response: {response}')
    print(f'Response : {response_hex}')


finally:
    # Close the serial port
    ser.close()


