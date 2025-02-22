# Seneca ZE-SG3 Modbus TCP Interface

## Overview
This Python script provides an interface for communicating with the **Seneca ZE-SG3** device using the **Modbus TCP** protocol. It allows users to read and write various registers on the device, such as machine ID, firmware version, measurement units, and more.

## Features
- Connects to the **Seneca ZE-SG3** using **Modbus TCP**.
- Reads and writes register values.
- Supports measurement unit configuration.
- Handles ADC speed, denoise filters, and resolution mode settings.

## Requirements
Ensure you have the following dependencies installed:

```sh
pip install pymodbus
```

## Installation
Clone this repository and navigate to the project directory:

```sh
git clone https://github.com/emoninet2/seneca-ze-sg3.git 
cd seneca-ze-sg3
```

## Usage
1. Create an instance of the **ZESG3** class.
2. Use the `open_server` method to establish a connection.
3. Interact with the device using available methods.

Example usage:

```python
from seneca import ZESG3

# Initialize device
device = ZESG3(host='192.168.1.100', port=502)

# Open connection
device.open_server()

# Read a register
firmware_version = device.read_firmware_version()
print(f"Firmware Version: {firmware_version}")

# Close connection
device.close_server()
```

## Error Handling
If the script encounters connection issues, ensure:
- The **ZE-SG3** device is powered on and accessible.
- The **IP address and port** are correct.
- The network allows Modbus TCP communication.

## Contributing
If you want to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Added new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Submit a pull request.

## License
This project is licensed under the **MIT License**.

## Contact
For support or inquiries, please contact [your.email@example.com](mailto:your.email@example.com).
