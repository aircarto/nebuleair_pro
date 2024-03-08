import serial

ser = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 2
)
   
# Send character 'S' to start the program
ser.write(b'\x81\x16\x69')      #state

# Read line   
while True:
    bs = ser.readline()
    print(bs)