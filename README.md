# IST AG Serial Line Data Logger for C4L Eval Board V1
This project provides a serial line data logger for the Innovative Sensor Technology (IST AG) C4L Eval Board V1. The logger captures various sensor readings, processes them, and stores the results in a JSON file with timestamps. It supports cleaning and storing data from the serial output, removing unnecessary spaces and ANSI escape sequences, and handling dynamic data storage with unique filenames.

## Requirements
- **Python 3.x**  
  Ensure you have Python 3.x installed on your system.
  
- **PySerial**  
  Install PySerial to enable serial communication:
  ```bash
  pip install pyserial

- **Regular Expressions (re)**
  This module is included by default in Python, so no separate installation is required.

- **Operating System**
  Works on Windows, Linux, and macOS as long as the correct serial port is find.

## Usage

1. **Connect the C4L Eval Board V1** to your computer via the serial port.
2. **Run the script**:
   ```bash
   python data_logger.py

  The logger will continuously read data from the serial port, clean the input, and save it to a unique .json file with a timestamp when the data exceeds a certain size or when manually stopped.

  3. **View the output: The script will output the captured and cleaned data to the console, and it will be saved in a new JSON file whenever the data reaches a size threshold. Example filename format:**
  ```bash
   data_output_YYYYMMDD_HHMMSS.json
  ```

  4. Stop the script:
  Press Ctrl+C to stop the logging process. The data will be saved at the moment of interruption.

## Data Output Format:
  The data will be saved in the following format in the .json file:
  ```json
{
  "Conductivity measured:": ["value1", "value2", ...],
  "Temperature Sensor:": ["value1", "value2", ...],
  "Conductivity T 25 C:": ["value1", "value2", ...],
  "Current I:": ["value1", "value2", ...],
  "Voltage Ui:": ["value1", "value2", ...],
  "Voltage Uo:": ["value1", "value2", ...],
  "Measurement range:": ["value1", "value2", ...]
}
  ```
  Excel 2016 and later versions allow you to import data directly from a JSON file. Here’s how a user can do it:
    1. Open Excel.
    2. Go to the “Data” tab.
    3. Click “Get Data” > “From File” > “From JSON”.
    4. Browse to the location of the JSON file and select it.
    5. Excel will parse the JSON and display the data in a table format, which you can then manipulate or save as an Excel file.
