'''
Script to read data from one NextPM and save the output to a JSON file

Need to install python3 and other libraries:
sudo apt install python3-pip
sudo pip3 install pyserial --break-system-packages
sudo pip3 install requests --break-system-packages
sudo pip3 install colorama --break-system-packages

Send data as a JSON:
{
  "capteurID": "nebuleairpro1",
  "data": [
    {
      "PM1": 0.9,
      "PM25": 1,
      "PM10": 0,
      "error_num": "000"
    },
    {
      "PM1": 1.2,
      "PM25": 1.7,
      "PM10": 5.2,
      "error_num": "000"
    },
    {
      "PM1": 1.4,
      "PM25": 2.4,
      "PM10": 2.4,
      "error_num": "000"
    }
  ]
}

'''

import serial
import time
import json
import time

start_time = time.time()

capteurID = 'nebuleairpro1'

#First NPM
ser_NPM1 = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 0.1
)

#Second NPM
ser_NPM2 = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 0.1
)

#Third NPM
ser_NPM3 = serial.Serial(
    port='/dev/ttyUSB3',
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 0.1
)


def read_serial_lines(ser):
    response_lines = []
    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            break 
        response_lines.append(line)
    return response_lines

nextPM_serlist = [ser_NPM1, ser_NPM2, ser_NPM3]
data = {'capteurID' : capteurID , 'data': []}
nextPM_id = 1

print("Starting script:")

for nextPM_ser in nextPM_serlist:

    #Write command to NextPM
    nextPM_ser.write(b'\x81\x12\x6D')     #data60s
    #Read response
    byte_data = nextPM_ser.readline()
    stateByte = int.from_bytes(byte_data[2:3], byteorder='big')
    Statebits = [int(bit) for bit in bin(stateByte)[2:].zfill(8)]
    PM1 = int.from_bytes(byte_data[9:11], byteorder='big')/10
    PM25 = int.from_bytes(byte_data[11:13], byteorder='big')/10
    PM10 = int.from_bytes(byte_data[13:15], byteorder='big')/10
    #create python object
    sensor_data = {
        'sondeID': 'NPM' + str(nextPM_id),
        'PM1': PM1,
        'PM25': PM25,
        'PM10': PM10,
        'err' : str(Statebits[0])+str(Statebits[1])+str(Statebits[2])
    }
    data['data'].append(sensor_data)
    nextPM_id = nextPM_id + 1
    nextPM_ser.close()

json_data = json.dumps(data) #convert python object to JSON
print(json_data)
JSON_lengh = len(json_data)
print("JSON lenght:" + str(JSON_lengh) )

########## save to file ###############

file_path = "nextpm/data.json"

try:
    # Open the file in write mode
    with open(file_path, 'w') as file:
        json.dump(data, file)
    print("JSON data has been saved to", file_path)
except Exception as e:
    print("An error occurred:", e)

end_time = time.time()

elapsed_time = end_time - start_time

print("Elapsed time: {:.2f} seconds".format(elapsed_time))
