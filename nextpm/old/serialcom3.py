import serial

#ser = serial.Serial('/dev/ttyUSB1', 115200 , timeout=1)

ser = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 1
)

   
packet = bytearray()
packet.append(0x81)
packet.append(0x16)
packet.append(0x69)

ser.write(packet)

# Read line   
while True:
    bs = ser.readline()
    print(bs)