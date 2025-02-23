import serial
import serial.tools.list_ports
import re
import json
import time

data_output = {
    'Conductivity measured:': [],
    'Temperature Sensor:': [],
    'Conductivity T 25 C:': [],
    'Current I:': [],
    'Voltage Ui:': [],
    'Voltage Uo:': [],
    'Measurement range:': []
}

def find_serial_port():
    """Automatically detect the serial port that corresponds to the C4L Eval Board V1."""
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        # Check if the port is related to the C4L Eval Board (you may adjust the device name or VID/PID)
        if 'USB Serial Port' in port.description or 'USB Serial' in port.description:
            return port.device
    raise Exception("C4L Eval Board not found. Please check the connection.")

def data_check():
    """Check if all 'Measurement range:' values are the same."""
    return all(x == data_output['Measurement range:'][0] for x in data_output['Measurement range:']) if data_output['Measurement range:'] else False

def clean_data(data, line_counter):
    """Clean the data by removing ANSI escape sequences and store values."""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')
    data = ansi_escape.sub('', data).strip()

    # Replace multiple spaces with a single space
    data = re.sub(r'\s+', ' ', data)

    if '25l' not in data:
        if data.startswith("1H"):
            name = data[2:-3].strip()
            print(line_counter, name)
        elif data.startswith("24H"):
            value = data[3:-4].strip()
            store_data(line_counter, value)

def store_data(line_counter, value):
    """Store the cleaned data in appropriate lists based on line counter."""
    if line_counter == 8 and 'mS/cm' in value:
        data_output['Conductivity measured:'].append(value)
    elif line_counter == 9 and 'C' in value:
        data_output['Temperature Sensor:'].append(value)
    elif line_counter == 10 and 'mS/cm' in value:
        data_output['Conductivity T 25 C:'].append(value)
    elif line_counter == 11 and 'mApp' in value:
        data_output['Current I:'].append(value)
    elif line_counter == 12 and 'mVpp' in value:
        data_output['Voltage Ui:'].append(value)
    elif line_counter == 13 and 'mVpp' in value:
        data_output['Voltage Uo:'].append(value)
    elif line_counter == 14:
        data_output['Measurement range:'].append(value)

    print(line_counter, value)

def save_data():
    """Save the data to a new file with a unique filename."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_path = f"data_output_{timestamp}.json"
    
    # Ensure file name is unique
    with open(file_path, 'w') as f:
        json.dump(data_output, f, indent=4)
    
    print(f"Data saved to {file_path}")

def reset_data():
    """Reset the values in data_output without clearing the keys."""
    for key in data_output:
        data_output[key] = []

def read_serial(port=None, baudrate=115200):
    """Read data from the serial port and process it."""    
    try:
        if port is None:
            port = find_serial_port()  # Automatically find the port if not provided

        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Reading from {port} at {baudrate} baud...")
            buffer = ""
            line_counter = 0

            while True:
                char = ser.read().decode('utf-8', errors='ignore')
                if char == ';':
                    clean_data(buffer, line_counter)

                    # Save data if the output exceeds a certain size
                    if len(str(data_output)) > 100000:  # You can adjust this threshold
                        save_data()
                        reset_data()  # Reset the lists without clearing keys

                    # Reset for next line
                    if line_counter < 14:
                        line_counter += 1
                    else:
                        line_counter = 0
                    buffer = ""
                else:
                    buffer += char

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nSerial reading stopped.")
        print(data_output)
        print(data_check())
        save_data()

if __name__ == "__main__":
    read_serial()
