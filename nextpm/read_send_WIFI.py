'''
Script to run every minutes as a cronjob:
* * * * * /usr/bin/python3 /home/nebuleairpro/nextpm/scanUSB.py

Read NextPM values over 3 USB ports and send them to aircarto's server via Ethernet/WIFI connexion

Need to install python3 and other libraries:
sudo apt install python3-pip
sudo pip3 install pyserial --break-system-packages
sudo pip3 install requests --break-system-packages

'''

import serial
import requests
import json

url = 'https://data.nebuleair.fr/pro_wifi.php'
headers = {'Content-Type': 'application/json'}

usbPorts = ['/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3']

for usb in usbPorts:
    ser = serial.Serial(
        port=usb,
        baudrate=115200,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = 2
    )

    #ser.write(b'\x81\x11\x6E')      #data10s
    ser.write(b'\x81\x12\x6D')      #data60s
        
    while True:
        try:
            byte_data = ser.readline()
            print(byte_data)
            stateByte = int.from_bytes(byte_data[2:3], byteorder='big')
            Statebits = [int(bit) for bit in bin(stateByte)[2:].zfill(8)]
            PM1 = int.from_bytes(byte_data[9:11], byteorder='big')/10
            PM25 = int.from_bytes(byte_data[11:13], byteorder='big')/10
            PM10 = int.from_bytes(byte_data[13:15], byteorder='big')/10
            print(f"State: {Statebits}")
            print(f"PM1: {PM1}")
            print(f"PM25: {PM25}")
            print(f"PM10: {PM10}")
            #create JSON            
            data = {
            'capteurID': 'nebuleairpro1',
            'sondeID':usb,
            'PM1': PM1,
            'PM25': PM25,
            'PM10': PM10,
            'sleep' : Statebits[0],
            'degradedState' : Statebits[1],
            'notReady' : Statebits[2],
            'heatError' : Statebits[3],
            't_rhError' : Statebits[4],
            'fanError' : Statebits[5],
            'memoryError' : Statebits[6],
            'laserError' : Statebits[7]
            }
            json_data = json.dumps(data)
            print(json_data)
            #send data
            response = requests.post(url, data=json_data, headers=headers)
            if response.status_code == 200:
                print('POST request successful!')
                #print('Response:', response.json())
            else:
                print('POST request failed. Status code:', response.status_code)
                print('Response:', response.text)
            break
        except:
            # for all other kinds of error, but not specifying which one
            print("Unknown error...")
            time.sleep(3)
            exit()
        finally:
            if ser.is_open:
                ser.close()
                print("Serial closed")