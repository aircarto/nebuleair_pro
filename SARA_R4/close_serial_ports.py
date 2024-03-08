import serial.tools.list_ports

def close_all_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device)
            ser.close()
            print(f"Closed serial port: {port.device}")
        except Exception as e:
            print(f"Error closing serial port {port.device}: {e}")

if __name__ == "__main__":
    close_all_serial_ports()
