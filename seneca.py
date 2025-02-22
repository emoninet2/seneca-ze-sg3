"""
Author: Habibur Rahman
Date: 9th Feb 2025
Description: This script provides an interface to communicate with the Seneca ZE-SG3 device using the Modbus TCP protocol.
             It includes functions to read and write various registers on the device, such as machine ID, firmware version,
             measurement unit, and more.

Usage:
    - Create an instance of the ZESG3 class.
    - Use the open_server method to connect to the device.
    - Use the provided methods to interact with the device.
    - Use the close_server method to disconnect from the device.

Example:
    ze_sg3 = ZESG3()
    ze_sg3.open_server("192.168.0.101", 502)
    machine_id = ze_sg3.get_machine_id()
    print(f"Machine ID: {machine_id}")
    ze_sg3.close_server()

Dependencies:
    - pymodbus
    - struct

License: MIT License
"""
from pymodbus.client import ModbusTcpClient as ModbusClient
import struct 

class register:
    MACHINE_ID = 0
    FIRMWARE_VERSION = 1
    MEASURE_UNIT = 2
    UNIPOLAR_BIPOLAR = 3
    ANALOG_OUTPUT_TYPE = 4
    DIGITAL_IN_TYPE = 5
    CALIBRATION_MODE = 6
    CELL_SENSE_RATIO_MSW = 13
    CELL_SENSE_RATIO_LSW = 14
    CELL_FULL_SCALE_MSW = 15
    CELL_FULL_SCALE_LSW = 16
    STADNDARD_WEIGHT_CELL_FLOAT_MSW = 17
    STADNDARD_WEIGHT_CELL_FLOAT_LSW = 18
    THRESHOLD_DO1_MSW = 19
    THRESHOLD_DO1_LSW = 20
    OUTPUT_WEIGHT_START_SCALE_MSW = 21
    OUTPUT_WEIGHT_START_SCALE_LSW = 22
    OUTPUT_WEIGHT_STOP_SCALE_MSW = 23
    OUTPUT_WEIGHT_STOP_SCALE_LSW = 24
    OUTPUT_STOP_SCALE_MSW = 25
    OUTPUT_STOP_SCALE_LSW = 26
    OUTPUT_START_SCALE_MSW = 27
    OUTPUT_START_SCALE_LSW = 28
    DELTA_WEIGHT_MSW = 29
    DELTA_WEIGHT_LSW = 30
    DELTA_TIME = 31
    DOUT_MODE = 32
    ADVANCED_ADC_SPEED = 33
    AUTOMATIC_TARE_RESET_MSW = 34
    AUTOMATIC_TARE_RESET_LSW = 35
    THRESHOLD_HYSTERESIS_DO1_MSW = 36
    THRESHOLD_HYSTERESIS_DO1_LSW = 37
    ADVANCED_DENOISE_FILTER_VARIATION_MSW = 38
    ADVANCED_DENOISE_FILTER_VARIATION_LSW = 39
    ADVANCED_DENOISE_FILTER_RESPONSE_MSW = 40
    ADVANCED_DENOISE_FILTER_RESPONSE_LSW = 41
    DENOISE_FILTER_VALUE = 42
    RESOLUTION_MODE = 43
    DENOISE_FILTER_ENABLE = 44
    MANUAL_RESOLUTION_MSW = 45
    MANUAL_RESOLUTION_LSW = 46
    ONE_PIECE_WEIGHT_MSW = 47
    ONE_PIECE_WEIGHT_LSW = 48
    THRESHOLD_DO2_MSW = 49
    THRESHOLD_DO2_LSW = 50
    THRESHOLD_HYSTERESIS_DO2_MSW = 51
    THRESHOLD_HYSTERESIS_DO2_LSW = 52
    ADC_FILTERED_16BIT = 62
    NET_WEIGHT_VALUE_MSW = 63
    NET_WEIGHT_VALUE_LSW = 64
    GROSS_WEIGHT_VALUE_MSW = 65
    GROSS_WEIGHT_VALUE_LSW = 66
    TARE_WEIGHT_VALUE_MSW = 67
    TARE_WEIGHT_VALUE_LSW = 68
    INTEGER_NET_WEIGHT_VALUE_MSW = 69
    INTEGER_NET_WEIGHT_VALUE_LSW = 70
    INTEGER_GROSS_WEIGHT_VALUE_MSW = 71
    INTEGER_GROSS_WEIGHT_VALUE_LSW = 72
    INTEGER_TARE_WEIGHT_VALUE_MSW = 73
    INTEGER_TARE_WEIGHT_VALUE_LSW = 74
    FACTORY_MANUAL_TARE_MSW = 75
    FACTORY_MANUAL_TARE_LSW = 76
    STATUS = 77
    PASSWORD = 78
    COMMAND_REGISTER = 79
    PIECES_NR = 80
    MAX_NET_WEIGHT_MSW = 81
    MAX_NET_WEIGHT_LSW = 82
    MIN_NET_WEIGHT_MSW = 83
    MIN_NET_WEIGHT_LSW = 84
    ADC_RAW_24BIT_MSW = 91
    ADC_RAW_24BIT_LSW = 92
    ADC_RAW_24BIT_FILTERED_MSW = 93
    ADC_RAW_24BIT_FILTERED_LSW = 94
    MODBUS_MANUAL_ANALOG_OUTPUT = 95


class measure_unit:
    kg = 0
    g = 1
    t = 2
    lb = 3
    l = 4
    N = 5
    bar = 6
    atm = 7
    other = 8

class advanced_adc_speed:
    _960Hz = 0
    _300Hz = 1
    _150Hz = 2
    _100Hz = 3
    _60Hz = 4
    _12Hz = 5
    _4_7Hz = 6


class denoise_filter_value:
    _2_0ms = 0
    _6_7ms = 1
    _13_0ms = 2
    _30_0ms = 3
    _50_0ms = 4
    _250_0ms = 5
    _850_0ms = 6
    advanced = 7


class resolution_mode:
    automatic = 0 #calculated on the basis of the full scale to obtain about 20000 points
    manual = 1 #taken from MANUAL RESOLUTION register
    max_resolution = 2 #full 24 bits


class command_register:
    reboot_device = 43948
    acquire_tare_in_RAM = 49594
    acquire_tare_in_FLASH_for_calibration = 49914
    acquire_sample_weight_in_FLASH_for_calibration = 50700
    acquire_tare_value_from_register = 50773
    reset_maximum_net_weight = 49151
    reset_register_with_minimum_net_weight = 45056


class ZESG3:
    def __init__(self, ip, port):
        self.client = None
        self.open_server(ip, port)

    def open_server(self, ip, port):
        """
        Opens the server for communication.

        Args:
            ip (str): IP address to bind the server to.
            port (int): Port number to bind the server to.

        Returns:
            None
        """
        self.client = ModbusClient(host=ip, port=port)  # Use keyword arguments
        if self.client.connect():
            print("Server opened successfully.")
        else:
            print("Failed to open server.")

    def close_server(self):
        """
        Closes the server for communication.

        Returns:
            None
        """
        self.client.close()
        print("Server closed successfully.")


    def test(self):
        result = self.client.read_holding_registers(0x0001, count=2)
        if result.isError():
            print("Test failed.")
        else:
            print(result.registers)

            
    def get_machine_id(self):
        """
        Retrieves the machine ID from the Seneca ZE-SG3 device.

        Returns:
            str: The machine ID as a string.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.MACHINE_ID, count=1)  # Reading 2 registers

        if result.isError():
            print("Failed to retrieve machine ID.")
            return None
        else:
            # get the 16-bit integer from the registers
            machine_id = result.registers[0]
            #machine_id = (result.registers[0] << 16) + result.registers[1]
            return machine_id  # Convert to hexadecimal string


    def get_firmware_version(self):
        """
        Retrieves the firmware version from the Seneca ZE-SG3 device.

        Returns:
            str: The firmware version as a string.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.FIRMWARE_VERSION, count=1)

        if result.isError():
            print("Failed to retrieve firmware version.")
            return None
        else:
            # get the 16-bit integer from the registers
            firmware_version = result.registers[0]
            return firmware_version


    def get_measurement_unit(self):
        """
        Retrieves the measurement unit from the Seneca ZE-SG3 device.

        Returns:
            str: The measurement unit as a string.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.MEASURE_UNIT, count=1)

        if result.isError():
            print("Failed to retrieve measurement unit.")
            return None
        else:
            # get the 16-bit integer from the registers
            measurement_unit = result.registers[0]
            return measurement_unit


    def set_measurement_unit(self, unit):
        """
        Sets the measurement unit on the Seneca ZE-SG3 device.

        Args:
            unit (str): The measurement unit to set.

        Returns:
            None
        """

        # Validate that the unit is a member of the measure_unit class
        if unit not in measure_unit.__dict__.values():
            print("Invalid measurement unit.")
            return
        

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.MEASURE_UNIT, unit)

        if result.isError():
            print("Failed to set measurement unit.")
        else:
            print("Measurement unit set successfully.")


    def get_unipolar_bipolar(self):
        """
        Retrieves the unipolar/bipolar setting from the Seneca ZE-SG3 device.

        Returns:
            str: The unipolar/bipolar setting as a string.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.UNIPOLAR_BIPOLAR, count=1)

        if result.isError():
            print("Failed to retrieve unipolar/bipolar setting.")
            return None
        else:
            # get the 16-bit integer from the registers
            unipolar_bipolar = result.registers[0]
            return unipolar_bipolar
        
    def set_unipolar_bipolar(self, setting):
        """
        Sets the unipolar/bipolar setting on the Seneca ZE-SG3 device.

        Args:
            setting (str): The unipolar/bipolar setting to set.

        Returns:
            None
        """
        # Replace with the actual register address and quantity
        result = self.client.write_register(register.UNIPOLAR_BIPOLAR, setting)

        if result.isError():
            print("Failed to set unipolar/bipolar setting.")
        else:
            print("Unipolar/bipolar setting set successfully.")



    def set_analog_output_type(self, output_type, output_linked_to):
        """
        Sets the analog output type on the Seneca ZE-SG3 device.

        Args:
            output_type (str): The analog output type to set.

        Returns:
            None
        """
        # Replace with the actual register address and quantity
    
        ANALOT_OUTPUT_TYPE_BP = 0
        ANALOG_OUTPUT_LINKED_TO_BP = 2

        value = output_type << ANALOT_OUTPUT_TYPE_BP | output_linked_to << ANALOG_OUTPUT_LINKED_TO_BP
        result = self.client.write_register(register.ANALOG_OUTPUT_TYPE, value)

        if result.isError():
            print("Failed to set analog output type.")
        else:
            print("Analog output type set successfully.")



    def get_analog_output_type(self):
        """
        Retrieves the analog output type from the Seneca ZE-SG3 device.

        Returns:
            str: The analog output type as a string.
        """

        ANALOG_OUTPUT_TYPE_BP = 0
        ANALOG_OUTPUT_LINKED_TO_BP = 2
        
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.ANALOG_OUTPUT_TYPE, count=1)
        

        if result.isError():
            print("Failed to retrieve analog output type.")
            return None
        else:
            # get the 16-bit integer from the registers
            analog_output_type = result.registers[0]
            output_type = analog_output_type >> ANALOG_OUTPUT_TYPE_BP
            output_linked_to = analog_output_type >> ANALOG_OUTPUT_LINKED_TO_BP
            return output_type, output_linked_to
        
    def set_digital_in_type(self, di1_type, di2_type, dio1_type, dio2_type):    
        """
        Sets the digital input type on the Seneca ZE-SG3 device.

        Args:
            di1_type (str): The digital input type on DIO1.
            di2_type (str): The digital input type on DIO2.
            dio1_type (str): Input/Output type on DIO1.
            dio2_type (str): Input/Output tyee on DIO2.

        Returns:
            None
        """

        DI_TYPE_BP = 8
        DI_TYPE_BP = 9
        DIO1_TYPE_BP = 0
        DIO2_TYPE_BP = 1

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.DIGITAL_IN_TYPE, di1_type << DI_TYPE_BP | di2_type << DI_TYPE_BP | dio1_type << DIO1_TYPE_BP | dio2_type << DIO2_TYPE_BP)

        if result.isError():
            print("Failed to set digital input type.")
        else:
            print("Digital input type set successfully.")


    def get_digital_in_type(self):
        """
        Retrieves the digital input type from the Seneca ZE-SG3 device.

        Returns:
            str: The digital input type as a string.
        """
        DI_TYPE_BP = 8
        DI_TYPE_BP = 9
        DIO1_TYPE_BP = 0
        DIO2_TYPE_BP = 1

        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.DIGITAL_IN_TYPE, count=1)

        if result.isError():
            print("Failed to retrieve digital input type.")
            return None
        else:
            # get the 16-bit integer from the registers
            digital_input_type = result.registers[0]
            di1_type = digital_input_type >> DI_TYPE_BP
            di2_type = digital_input_type >> DI_TYPE_BP
            dio1_type = digital_input_type >> DIO1_TYPE_BP
            dio2_type = digital_input_type >> DIO2_TYPE_BP
            return di1_type, di2_type, dio1_type, dio2_type
        


    def set_calibration_mode(self, mode):
        """
        Sets the calibration mode on the Seneca ZE-SG3 device.

        Args:
            mode (str): The calibration mode to set.

        Returns:
            None
        """
        # Replace with the actual register address and quantity
        result = self.client.write_register(register.CALIBRATION_MODE, mode)

        if result.isError():
            print("Failed to set calibration mode.")
        else:
            print("Calibration mode set successfully.")


    def get_calibration_mode(self):
        """
        Retrieves the calibration mode from the Seneca ZE-SG3 device.

        Returns:
            str: The calibration mode as a string.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.CALIBRATION_MODE, count=1)

        if result.isError():
            print("Failed to retrieve calibration mode.")
            return None
        else:
            # get the 16-bit integer from the registers
            calibration_mode = result.registers[0]
            return calibration_mode
        

    def set_cell_sense_ratio(self, ratio_f32):
        """
        Sets the cell sense ratio on the Seneca ZE-SG3 device.

        Args:
            ratio_f32 (float): The cell sense ratio to set.

        Returns:
            None
        """
        cell_sense_ratio_msw = self._float32_to_hex(ratio_f32) >> 16
        cell_sense_ratio_lsw = self._float32_to_hex(ratio_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.CELL_SENSE_RATIO_MSW, cell_sense_ratio_msw)
        result = self.client.write_register(register.CELL_SENSE_RATIO_LSW, cell_sense_ratio_lsw)

        if result.isError():
            print("Failed to set cell sense ratio.")
        else:
            print("Cell sense ratio set successfully.")


    def get_cell_sense_ratio(self):
        """
        Retrieves the cell sense ratio from the Seneca ZE-SG3 device.

        Returns:
            str: The cell sense ratio as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.CELL_SENSE_RATIO_MSW, count=2)

        if result.isError():
            print("Failed to retrieve cell sense ratio.")
            return None
        else:
            # get the 16-bit integer from the registers
            cell_sense_ratio_msw = result.registers[0]
            cell_sense_ratio_lsw = result.registers[1]
            return self._hex_to_float32((cell_sense_ratio_msw << 16) + cell_sense_ratio_lsw)

        
    def set_cell_full_scale(self, full_scale_f32):
        """
        Sets the cell full scale on the Seneca ZE-SG3 device.

        Args:
            full_scale_f32 (float): The cell full scale to set.

        Returns:
            None
        """
        cell_full_scale_msw = self._float32_to_hex(full_scale_f32) >> 16
        cell_full_scale_lsw = self._float32_to_hex(full_scale_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.CELL_FULL_SCALE_MSW, cell_full_scale_msw)
        result = self.client.write_register(register.CELL_FULL_SCALE_LSW, cell_full_scale_lsw)

        if result.isError():
            print("Failed to set cell full scale.")
        else:
            print("Cell full scale set successfully.")



    def get_cell_full_scale(self):
        """
        Retrieves the cell full scale from the Seneca ZE-SG3 device.

        Returns:
            str: The cell full scale as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.CELL_FULL_SCALE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve cell full scale.")
            return None
        else:
            # get the 16-bit integer from the registers
            cell_full_scale_msw = result.registers[0]
            cell_full_scale_lsw = result.registers[1]
            return self._hex_to_float32((cell_full_scale_msw << 16) + cell_full_scale_lsw)


    def set_standard_weight_cell_float(self, weight_f32):
        """
        Sets the standard weight cell float on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The standard weight cell float to set.

        Returns:
            None
        """
        standard_weight_cell_float_msw = self._float32_to_hex(weight_f32) >> 16
        standard_weight_cell_float_lsw = self._float32_to_hex(weight_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.STADNDARD_WEIGHT_CELL_FLOAT_MSW, standard_weight_cell_float_msw)
        result = self.client.write_register(register.STADNDARD_WEIGHT_CELL_FLOAT_LSW, standard_weight_cell_float_lsw)

        if result.isError():
            print("Failed to set standard weight cell float.")
        else:
            print("Standard weight cell float set successfully.")





    def get_standard_weight_cell_float(self):
        """
        Retrieves the standard weight cell float from the Seneca ZE-SG3 device.

        Returns:
            str: The standard weight cell float as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.STADNDARD_WEIGHT_CELL_FLOAT_MSW, count=2)

        if result.isError():
            print("Failed to retrieve standard weight cell float.")
            return None
        else:
            # get the 16-bit integer from the registers
            standard_weight_cell_float_msw = result.registers[0]
            standard_weight_cell_float_lsw = result.registers[1]
            return self._hex_to_float32((standard_weight_cell_float_msw << 16) + standard_weight_cell_float_lsw)


    def set_threshold_do1(self, threshold_f32):
        """
        Sets the threshold DO1 on the Seneca ZE-SG3 device.

        Args:
            threshold_f32 (float): The threshold DO1 to set.

        Returns:
            None
        """
        threshold_do1_msw = self._float32_to_hex(threshold_f32) >> 16
        threshold_do1_lsw = self._float32_to_hex(threshold_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.THRESHOLD_DO1_MSW, threshold_do1_msw)
        result = self.client.write_register(register.THRESHOLD_DO1_LSW, threshold_do1_lsw)

        if result.isError():
            print("Failed to set threshold DO1.")
        else:
            print("Threshold DO1 set successfully.")



    def get_threshold_do1(self):
        """
        Retrieves the threshold DO1 from the Seneca ZE-SG3 device.

        Returns:
            str: The threshold DO1 as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.THRESHOLD_DO1_MSW, count=2)

        if result.isError():
            print("Failed to retrieve threshold DO1.")
            return None
        else:
            # get the 16-bit integer from the registers
            threshold_do1_msw = result.registers[0]
            threshold_do1_lsw = result.registers[1]
            return self._hex_to_float32((threshold_do1_msw << 16) + threshold_do1_lsw)



    def set_output_weight_start_scale(self, value_f32):
        """
        Sets the output weight start scale on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The output weight start scale to set.

        Returns:
            None
        """
        output_weight_start_scale_msw = self._float32_to_hex(value_f32) >> 16
        output_weight_start_scale_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.OUTPUT_WEIGHT_START_SCALE_MSW, output_weight_start_scale_msw)
        result = self.client.write_register(register.OUTPUT_WEIGHT_START_SCALE_LSW, output_weight_start_scale_lsw)

        if result.isError():
            print("Failed to set output weight start scale.")
        else:
            print("Output weight start scale set successfully.")



    def get_output_weight_start_scale(self):
        """
        Retrieves the output weight start scale from the Seneca ZE-SG3 device.

        Returns:
            str: The output weight start scale as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.OUTPUT_WEIGHT_START_SCALE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve output weight start scale.")
            return None
        else:
            # get the 16-bit integer from the registers
            output_weight_start_scale_msw = result.registers[0]
            output_weight_start_scale_lsw = result.registers[1]
            return self._hex_to_float32((output_weight_start_scale_msw << 16) + output_weight_start_scale_lsw)



    def set_output_weight_stop_scale(self, value_f32):
        """
        Sets the output weight stop scale on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The output weight stop scale to set.

        Returns:
            None
        """
        output_weight_stop_scale_msw = self._float32_to_hex(value_f32) >> 16
        output_weight_stop_scale_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.OUTPUT_WEIGHT_STOP_SCALE_MSW, output_weight_stop_scale_msw)
        result = self.client.write_register(register.OUTPUT_WEIGHT_STOP_SCALE_LSW, output_weight_stop_scale_lsw)

        if result.isError():
            print("Failed to set output weight stop scale.")
        else:
            print("Output weight stop scale set successfully.")


    def get_output_weight_stop_scale(self):
        """
        Retrieves the output weight stop scale from the Seneca ZE-SG3 device.

        Returns:
            str: The output weight stop scale as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.OUTPUT_WEIGHT_STOP_SCALE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve output weight stop scale.")
            return None
        else:
            # get the 16-bit integer from the registers
            output_weight_stop_scale_msw = result.registers[0]
            output_weight_stop_scale_lsw = result.registers[1]
            return self._hex_to_float32((output_weight_stop_scale_msw << 16) + output_weight_stop_scale_lsw)
        



    def set_output_stop_scale(self, value_f32):
        """
        Sets the output stop scale on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The output stop scale to set.

        Returns:
            None
        """
        output_stop_scale_msw = self._float32_to_hex(value_f32) >> 16
        output_stop_scale_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.OUTPUT_STOP_SCALE_MSW, output_stop_scale_msw)
        result = self.client.write_register(register.OUTPUT_STOP_SCALE_LSW, output_stop_scale_lsw)

        if result.isError():
            print("Failed to set output stop scale.")
        else:
            print("Output stop scale set successfully.")



    def get_output_stop_scale(self):
        """
        Retrieves the output stop scale from the Seneca ZE-SG3 device.

        Returns:
            str: The output stop scale as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.OUTPUT_STOP_SCALE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve output stop scale.")
            return None
        else:
            # get the 16-bit integer from the registers
            output_stop_scale_msw = result.registers[0]
            output_stop_scale_lsw = result.registers[1]
            return self._hex_to_float32((output_stop_scale_msw << 16) + output_stop_scale_lsw)



    def set_output_start_scale(self, value_f32):
        """
        Sets the output start scale on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The output start scale to set.

        Returns:
            None
        """
        output_start_scale_msw = self._float32_to_hex(value_f32) >> 16
        output_start_scale_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.OUTPUT_START_SCALE_MSW, output_start_scale_msw)
        result = self.client.write_register(register.OUTPUT_START_SCALE_LSW, output_start_scale_lsw)

        if result.isError():
            print("Failed to set output start scale.")
        else:
            print("Output start scale set successfully.")


    def get_output_start_scale(self):
        """
        Retrieves the output start scale from the Seneca ZE-SG3 device.

        Returns:
            str: The output start scale as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.OUTPUT_START_SCALE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve output start scale.")
            return None
        else:
            # get the 16-bit integer from the registers
            output_start_scale_msw = result.registers[0]
            output_start_scale_lsw = result.registers[1]
            return self._hex_to_float32((output_start_scale_msw << 16) + output_start_scale_lsw)



    def set_delta_weight(self, value_f32):
        """
        Sets the delta weight on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The delta weight to set.

        Returns:
            None
        """
        delta_weight_msw = self._float32_to_hex(value_f32) >> 16
        delta_weight_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.DELTA_WEIGHT_MSW, delta_weight_msw)
        result = self.client.write_register(register.DELTA_WEIGHT_LSW, delta_weight_lsw)

        if result.isError():
            print("Failed to set delta weight.")
        else:
            print("Delta weight set successfully.")


    def get_delta_weight(self):
        """
        Retrieves the delta weight from the Seneca ZE-SG3 device.

        Returns:
            str: The delta weight as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.DELTA_WEIGHT_MSW, count=2)

        if result.isError():
            print("Failed to retrieve delta weight.")
            return None
        else:
            # get the 16-bit integer from the registers
            delta_weight_msw = result.registers[0]
            delta_weight_lsw = result.registers[1]
            return self._hex_to_float32((delta_weight_msw << 16) + delta_weight_lsw)
        


    def set_delta_time(self, time):
        """
        Sets the delta time on the Seneca ZE-SG3 device.

        Args:
            time (int): The delta time to set.

        Returns:
            None
        """
        # Replace with the actual register address and quantity
        result = self.client.write_register(register.DELTA_TIME, time)

        if result.isError():
            print("Failed to set delta time.")
        else:
            print("Delta time set successfully.")



    def get_delta_time(self):
        """
        Retrieves the delta time from the Seneca ZE-SG3 device.

        Returns:
            str: The delta time as an integer.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.DELTA_TIME, count=1)

        if result.isError():
            print("Failed to retrieve delta time.")
            return None
        else:
            # get the 16-bit integer from the registers
            delta_time = result.registers[0]
            return delta_time
        

    
    def set_dout_mode(self, dout1_openClose, dout2_openClose, dout1_mode, dout2_mode):
        """
        Sets the DOUT mode on the Seneca ZE-SG3 device.

        Args:
            dout1_openClose (str): The DOUT1 open/close mode.
            dout2_openClose (str): The DOUT2 open/close mode.
            dout1_mode (str): The DOUT1 mode.
            dout2_mode (str): The DOUT2 mode.

        Returns:
            None
        """
        DOUT1_OPEN_CLOSE_BP = 0
        DOUT2_OPEN_CLOSE_BP = 1
        DOUT1_MODE_BP = 11
        DOUT2_MODE_BP = 15

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.DOUT_MODE, dout1_openClose << DOUT1_OPEN_CLOSE_BP | dout2_openClose << DOUT2_OPEN_CLOSE_BP | (dout1_mode & 0x000F) << DOUT1_MODE_BP | (dout2_mode & 0x000F) << DOUT2_MODE_BP)

        if result.isError():
            print("Failed to set DOUT mode.")
        else:
            print("DOUT mode set successfully.")


    def get_dout_mode(self):
        """
        Retrieves the DOUT mode from the Seneca ZE-SG3 device.

        Returns:
            str: The DOUT mode as a string.
        """
        DOUT1_OPEN_CLOSE_BP = 0
        DOUT2_OPEN_CLOSE_BP = 1
        DOUT1_MODE_BP = 11
        DOUT2_MODE_BP = 15

        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.DOUT_MODE, count=1)

        if result.isError():
            print("Failed to retrieve DOUT mode.")
            return None
        else:
            # get the 16-bit integer from the registers
            dout_mode = result.registers[0]
            dout1_openClose = dout_mode >> DOUT1_OPEN_CLOSE_BP
            dout2_openClose = dout_mode >> DOUT2_OPEN_CLOSE_BP
            dout1_mode = dout_mode >> DOUT1_MODE_BP
            dout2_mode = dout_mode >> DOUT2_MODE_BP
            return dout1_openClose, dout2_openClose, dout1_mode, dout2_mode



    def set_advanced_adc_speed(self, speed):
        """
        Sets the advanced ADC speed on the Seneca ZE-SG3 device.

        Args:
            speed (int): The advanced ADC speed to set.

        Returns:
            None
        """
        # Replace with the actual register address and quantity
        result = self.client.write_register(register.ADVANCED_ADC_SPEED, speed)

        if result.isError():
            print("Failed to set advanced ADC speed.")
        else:
            print("Advanced ADC speed set successfully.")



    def get_advanced_adc_speed(self):
        """
        Retrieves the advanced ADC speed from the Seneca ZE-SG3 device.

        Returns:
            str: The advanced ADC speed as an integer.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.ADVANCED_ADC_SPEED, count=1)

        if result.isError():
            print("Failed to retrieve advanced ADC speed.")
            return None
        else:
            # get the 16-bit integer from the registers
            advanced_adc_speed = result.registers[0]
            return advanced_adc_speed
        
    def set_automatic_tare_reset(self, value):
        """
        Sets the automatic tare reset on the Seneca ZE-SG3 device.

        Args:
            value_f32 (float): The automatic tare reset to set.

        Returns:
            None
        """
        automatic_tare_reset_msw = (value) >> 16
        automatic_tare_reset_lsw = (value) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.AUTOMATIC_TARE_RESET_MSW, automatic_tare_reset_msw)
        result = self.client.write_register(register.AUTOMATIC_TARE_RESET_LSW, automatic_tare_reset_lsw)

        if result.isError():
            print("Failed to set automatic tare reset.")
        else:
            print("Automatic tare reset set successfully.")


    def get_automatic_tare_reset(self):
        """
        Retrieves the automatic tare reset from the Seneca ZE-SG3 device.

        Returns:
            str: The automatic tare reset as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.AUTOMATIC_TARE_RESET_MSW, count=2)

        if result.isError():
            print("Failed to retrieve automatic tare reset.")
            return None
        else:
            # get the 16-bit integer from the registers
            automatic_tare_reset_msw = result.registers[0]
            automatic_tare_reset_lsw = result.registers[1]
            return ((automatic_tare_reset_msw << 16) + automatic_tare_reset_lsw)


    def set_threshold_hysteresis_do1(self, value_f32):
        """
        Sets the threshold hysteresis DO1 on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The threshold hysteresis DO1 to set.

        Returns:
            None
        """
        threshold_hysteresis_do1_msw = self._float32_to_hex(value_f32) >> 16
        threshold_hysteresis_do1_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.THRESHOLD_HYSTERESIS_DO1_MSW, threshold_hysteresis_do1_msw)
        result = self.client.write_register(register.THRESHOLD_HYSTERESIS_DO1_LSW, threshold_hysteresis_do1_lsw)

        if result.isError():
            print("Failed to set threshold hysteresis DO1.")
        else:
            print("Threshold hysteresis DO1 set successfully.")


    def get_threshold_hysteresis_do1(self):
        """
        Retrieves the threshold hysteresis DO1 from the Seneca ZE-SG3 device.

        Returns:
            str: The threshold hysteresis DO1 as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.THRESHOLD_HYSTERESIS_DO1_MSW, count=2)

        if result.isError():
            print("Failed to retrieve threshold hysteresis DO1.")
            return None
        else:
            # get the 16-bit integer from the registers
            threshold_hysteresis_do1_msw = result.registers[0]
            threshold_hysteresis_do1_lsw = result.registers[1]
            return self._hex_to_float32((threshold_hysteresis_do1_msw << 16) + threshold_hysteresis_do1_lsw)


    
    def advanced_denoise_filter_variation(self, value_f32):
        """
        Sets the advanced denoise filter variation on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The advanced denoise filter variation to set.

        Returns:
            None
        """
        advanced_denoise_filter_variation_msw = self._float32_to_hex(value_f32) >> 16
        advanced_denoise_filter_variation_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.ADVANCED_DENOISE_FILTER_VARIATION_MSW, advanced_denoise_filter_variation_msw)
        result = self.client.write_register(register.ADVANCED_DENOISE_FILTER_VARIATION_LSW, advanced_denoise_filter_variation_lsw)

        if result.isError():
            print("Failed to set advanced denoise filter variation.")
        else:
            print("Advanced denoise filter variation set successfully.")


    def advanced_denoise_filter_variation(self):
        """
        Retrieves the advanced denoise filter variation from the Seneca ZE-SG3 device.

        Returns:
            str: The advanced denoise filter variation as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.ADVANCED_DENOISE_FILTER_VARIATION_MSW, count=2)

        if result.isError():
            print("Failed to retrieve advanced denoise filter variation.")
            return None
        else:
            # get the 16-bit integer from the registers
            advanced_denoise_filter_variation_msw = result.registers[0]
            advanced_denoise_filter_variation_lsw = result.registers[1]
            return self._hex_to_float32((advanced_denoise_filter_variation_msw << 16) + advanced_denoise_filter_variation_lsw)


    def set_advanced_denoise_filter_response(self, value_f32):
        """
        Sets the advanced denoise filter response on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The advanced denoise filter response to set.

        Returns:
            None
        """
        advanced_denoise_filter_response_msw = self._float32_to_hex(value_f32) >> 16
        advanced_denoise_filter_response_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.ADVANCED_DENOISE_FILTER_RESPONSE_MSW, advanced_denoise_filter_response_msw)
        result = self.client.write_register(register.ADVANCED_DENOISE_FILTER_RESPONSE_LSW, advanced_denoise_filter_response_lsw)

        if result.isError():
            print("Failed to set advanced denoise filter response.")
        else:
            print("Advanced denoise filter response set successfully.")


    def get_advanced_denoise_filter_response(self):
        """
        Retrieves the advanced denoise filter response from the Seneca ZE-SG3 device.

        Returns:
            str: The advanced denoise filter response as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.ADVANCED_DENOISE_FILTER_RESPONSE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve advanced denoise filter response.")
            return None
        else:
            # get the 16-bit integer from the registers
            advanced_denoise_filter_response_msw = result.registers[0]
            advanced_denoise_filter_response_lsw = result.registers[1]
            return self._hex_to_float32((advanced_denoise_filter_response_msw << 16) + advanced_denoise_filter_response_lsw)


    def set_denoise_filter_value(self, filter_value):
        """
        Sets the denoise filter value on the Seneca ZE-SG3 device.

        Args:
            value (int): The denoise filter value to set.

        Returns:
            None
        """
        
        if filter_value not in denoise_filter_value.__dict__.values():
            print("Invalid denoise filter value.")
            return

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.DENOISE_FILTER_VALUE, filter_value)

        if result.isError():
            print("Failed to set denoise filter value.")
        else:
            print("Denoise filter value set successfully.")

    def get_denoise_filter_value(self):
        """
        Retrieves the denoise filter value from the Seneca ZE-SG3 device.

        Returns:
            str: The denoise filter value as a string.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.DENOISE_FILTER_VALUE, count=1)

        if result.isError():
            print("Failed to retrieve denoise filter value.")
            return None
        else:
            # get the 16-bit integer from the registers
            denoise_filter_value = result.registers[0]
            return denoise_filter_value



    def set_resolution_mode(self, resolution_mode):
        """
        Sets the resolution mode on the Seneca ZE-SG3 device.

        Args:
            resolution_mode (int): The resolution mode to set.

        Returns:
            None
        """

        if resolution_mode not in resolution_mode.__dict__.values():
            print("Invalid resolution mode.")
            return

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.RESOLUTION_MODE, resolution_mode)

        if result.isError():
            print("Failed to set resolution mode.")
        else:
            print("Resolution mode set successfully.")



    def get_resolution_mode(self):
        """
        Retrieves the resolution mode from the Seneca ZE-SG3 device.

        Returns:
            str: The resolution mode as a string.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.RESOLUTION_MODE, count=1)

        if result.isError():
            print("Failed to retrieve resolution mode.")
            return None
        else:
            # get the 16-bit integer from the registers
            resolution_mode = result.registers[0]
            return resolution_mode
        

    def set_denoise_filter_enable(self, enable):
        """
        Enables or disables the denoise filter on the Seneca ZE-SG3 device.

        Args:
            enable (bool): True to enable the denoise filter, False to disable it.

        Returns:
            None
        """
        # Replace with the actual register address and quantity
        result = self.client.write_register(register.DENOISE_FILTER_ENABLE, enable)

        if result.isError():
            print("Failed to enable/disable denoise filter.")
        else:
            print("Denoise filter enabled/disabled successfully.")

    def get_denoise_filter_enable(self):
        """
        Retrieves the denoise filter enable status from the Seneca ZE-SG3 device.

        Returns:
            bool: True if the denoise filter is enabled, False otherwise.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.DENOISE_FILTER_ENABLE, count=1)

        if result.isError():
            print("Failed to retrieve denoise filter enable status.")
            return None
        else:
            # get the 16-bit integer from the registers
            denoise_filter_enable = result.registers[0]
            return denoise_filter_enable
        


    def set_manual_resolution(self, resolution_f32):
        """
        Sets the manual resolution on the Seneca ZE-SG3 device.

        Args:
            resolution_f32 (float): The manual resolution to set.

        Returns:
            None
        """
        manual_resolution_msw = self._float32_to_hex(resolution_f32) >> 16
        manual_resolution_lsw = self._float32_to_hex(resolution_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.MANUAL_RESOLUTION_MSW, manual_resolution_msw)
        result = self.client.write_register(register.MANUAL_RESOLUTION_LSW, manual_resolution_lsw)

        if result.isError():
            print("Failed to set manual resolution.")
        else:
            print("Manual resolution set successfully.")


    def get_manual_resolution(self):
        """
        Retrieves the manual resolution from the Seneca ZE-SG3 device.

        Returns:
            str: The manual resolution as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.MANUAL_RESOLUTION_MSW, count=2)

        if result.isError():
            print("Failed to retrieve manual resolution.")
            return None
        else:
            # get the 16-bit integer from the registers
            manual_resolution_msw = result.registers[0]
            manual_resolution_lsw = result.registers[1]
            return self._hex_to_float32((manual_resolution_msw << 16) + manual_resolution_lsw)


    def set_one_piece_weight(self, value_f32):
        """
        Sets the one piece weight on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The one piece weight to set.

        Returns:
            None
        """
        one_piece_weight_msw = self._float32_to_hex(value_f32) >> 16
        one_piece_weight_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.ONE_PIECE_WEIGHT_MSW, one_piece_weight_msw)
        result = self.client.write_register(register.ONE_PIECE_WEIGHT_LSW, one_piece_weight_lsw)

        if result.isError():
            print("Failed to set one piece weight.")
        else:
            print("One piece weight set successfully.")


    def get_one_piece_weight(self):
        """
        Retrieves the one piece weight from the Seneca ZE-SG3 device.

        Returns:
            str: The one piece weight as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.ONE_PIECE_WEIGHT_MSW, count=2)

        if result.isError():
            print("Failed to retrieve one piece weight.")
            return None
        else:
            # get the 16-bit integer from the registers
            one_piece_weight_msw = result.registers[0]
            one_piece_weight_lsw = result.registers[1]
            return self._hex_to_float32((one_piece_weight_msw << 16) + one_piece_weight_lsw)
        

    def set_threshold_do2(self, threshold_f32):
        """
        Sets the threshold DO2 on the Seneca ZE-SG3 device.

        Args:
            threshold_f32 (float): The threshold DO2 to set.

        Returns:
            None
        """
        threshold_do2_msw = self._float32_to_hex(threshold_f32) >> 16
        threshold_do2_lsw = self._float32_to_hex(threshold_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.THRESHOLD_DO2_MSW, threshold_do2_msw)
        result = self.client.write_register(register.THRESHOLD_DO2_LSW, threshold_do2_lsw)

        if result.isError():
            print("Failed to set threshold DO2.")
        else:
            print("Threshold DO2 set successfully.")


    def get_threshold_do2(self):
        """
        Retrieves the threshold DO2 from the Seneca ZE-SG3 device.

        Returns:
            str: The threshold DO2 as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.THRESHOLD_DO2_MSW, count=2)

        if result.isError():
            print("Failed to retrieve threshold DO2.")
            return None
        else:
            # get the 16-bit integer from the registers
            threshold_do2_msw = result.registers[0]
            threshold_do2_lsw = result.registers[1]
            return self._hex_to_float32((threshold_do2_msw << 16) + threshold_do2_lsw)


    def set_threshold_hysteresis_do2(self, value_f32):
        """
        Sets the threshold hysteresis DO2 on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The threshold hysteresis DO2 to set.

        Returns:
            None
        """
        threshold_hysteresis_do2_msw = self._float32_to_hex(value_f32) >> 16
        threshold_hysteresis_do2_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.THRESHOLD_HYSTERESIS_DO2_MSW, threshold_hysteresis_do2_msw)
        result = self.client.write_register(register.THRESHOLD_HYSTERESIS_DO2_LSW, threshold_hysteresis_do2_lsw)

        if result.isError():
            print("Failed to set threshold hysteresis DO2.")
        else:
            print("Threshold hysteresis DO2 set successfully.")


    def get_threshold_hysteresis_do2(self):
        """
        Retrieves the threshold hysteresis DO2 from the Seneca ZE-SG3 device.

        Returns:
            str: The threshold hysteresis DO2 as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.THRESHOLD_HYSTERESIS_DO2_MSW, count=2)

        if result.isError():
            print("Failed to retrieve threshold hysteresis DO2.")
            return None
        else:
            # get the 16-bit integer from the registers
            threshold_hysteresis_do2_msw = result.registers[0]
            threshold_hysteresis_do2_lsw = result.registers[1]
            return self._hex_to_float32((threshold_hysteresis_do2_msw << 16) + threshold_hysteresis_do2_lsw)


    def get_adc_filtered_16bit(self):
        """
        Retrieves the filtered ADC value from the Seneca ZE-SG3 device.

        Returns:
            str: The filtered ADC value as a 16-bit integer.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.ADC_FILTERED_16BIT, count=1)

        if result.isError():
            print("Failed to retrieve filtered ADC value.")
            return None
        else:
            # get the 16-bit integer from the registers
            adc_filtered_16bit = result.registers[0]
            return adc_filtered_16bit




    def get_net_weight_value(self):
        """
        Retrieves the net weight value from the Seneca ZE-SG3 device.

        Returns:
            str: The net weight value as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.NET_WEIGHT_VALUE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve net weight value.")
            return None
        else:
            # get the 16-bit integer from the registers
            net_weight_value_msw = result.registers[0]
            net_weight_value_lsw = result.registers[1]
            return self._hex_to_float32((net_weight_value_msw << 16) + net_weight_value_lsw)

    


    def get_gross_weight_value(self):
        """
        Retrieves the gross weight value from the Seneca ZE-SG3 device.

        Returns:
            str: The gross weight value as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.GROSS_WEIGHT_VALUE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve gross weight value.")
            return None
        else:
            # get the 16-bit integer from the registers
            gross_weight_value_msw = result.registers[0]
            gross_weight_value_lsw = result.registers[1]
            return self._hex_to_float32((gross_weight_value_msw << 16) + gross_weight_value_lsw)
        




    def get_tare_weight_value(self):
        """
        Retrieves the tare weight value from the Seneca ZE-SG3 device.

        Returns:
            str: The tare weight value as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.TARE_WEIGHT_VALUE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve tare weight value.")
            return None
        else:
            # get the 16-bit integer from the registers
            tare_weight_value_msw = result.registers[0]
            tare_weight_value_lsw = result.registers[1]
            return self._hex_to_float32((tare_weight_value_msw << 16) + tare_weight_value_lsw)
        



    def get_integer_net_weight_value(self):
        """
        Retrieves the integer net weight value from the Seneca ZE-SG3 device.

        Returns:
            str: The integer net weight value as an integer.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.INTEGER_NET_WEIGHT_VALUE, count=2)

        if result.isError():
            print("Failed to retrieve integer net weight value.")
            return None
        else:
            # Combine the two 16-bit registers into a 32-bit integer
            msw = result.registers[0]
            lsw = result.registers[1]
            integer_net_weight_value = (msw << 16) | lsw

            # Convert to a signed 32-bit integer if necessary
            if integer_net_weight_value >= 0x80000000:
                integer_net_weight_value -= 0x100000000

            return integer_net_weight_value




    def get_integer_gross_weight_value(self):
        """
        Retrieves the integer gross weight value from the Seneca ZE-SG3 device.

        Returns:
            str: The integer gross weight value as an integer.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.INTEGER_GROSS_WEIGHT_VALUE, count=2)

        if result.isError():
            print("Failed to retrieve integer gross weight value.")
            return None
        else:
            # Combine the two 16-bit registers into a 32-bit integer
            msw = result.registers[0]
            lsw = result.registers[1]
            integer_gross_weight_value = (msw << 16) | lsw

            # Convert to a signed 32-bit integer if necessary
            if integer_gross_weight_value >= 0x80000000:
                integer_gross_weight_value -= 0x100000000

            return integer_gross_weight_value



    def set_factory_manual_tare(self,value_f32):
        """
        Sets the factory manual tare on the Seneca ZE-SG3 device.

        Args:
            weight_f32 (float): The factory manual tare to set.

        Returns:
            None
        """
        factory_manual_tare_msw = self._float32_to_hex(value_f32) >> 16
        factory_manual_tare_lsw = self._float32_to_hex(value_f32) & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.FACTORY_MANUAL_TARE_MSW, factory_manual_tare_msw)
        result = self.client.write_register(register.FACTORY_MANUAL_TARE_LSW, factory_manual_tare_lsw)

        if result.isError():
            print("Failed to set factory manual tare.")
        else:
            print("Factory manual tare set successfully.")


    def get_factory_manual_tare(self):
        """
        Retrieves the factory manual tare from the Seneca ZE-SG3 device.

        Returns:
            str: The factory manual tare as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.FACTORY_MANUAL_TARE_MSW, count=2)

        if result.isError():
            print("Failed to retrieve factory manual tare.")
            return None
        else:
            # get the 16-bit integer from the registers
            factory_manual_tare_msw = result.registers[0]
            factory_manual_tare_lsw = result.registers[1]
            return self._hex_to_float32((factory_manual_tare_msw << 16) + factory_manual_tare_lsw)
        


    def get_status(self):
        """
        Retrieves the status from the Seneca ZE-SG3 device.

        Returns:
            dict: The status as a dictionary with integer values.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.STATUS, count=1)

        if result.isError():
            print("Failed to retrieve status.")
            return None
        else:
            # Get the 16-bit integer from the registers
            status_reg = result.registers[0]
            status = {
                'threshold_and_stable_weight_for_dido1': (status_reg >> 0) & 0x01,
                'full_scale_cell': (status_reg >> 1) & 0x01,
                'net_weight_less_than_zero': (status_reg >> 2) & 0x01,
                'threshold_and_stable_weight_for_dido2': (status_reg >> 3) & 0x01,
                'stable_weight': (status_reg >> 4) & 0x01,
                'digital_output_2_on': (status_reg >> 5) & 0x01,
                'digital_output_1_on': (status_reg >> 6) & 0x01,
                'threshold_with_hysteresis_for_dido1': (status_reg >> 7) & 0x01,
                'tare_tracker': (status_reg >> 8) & 0x01,
                'threshold_with_hysteresis_for_dido2': (status_reg >> 9) & 0x01,
            }

            return status


    def get_password(self):
        """
        Retrieves the password from the Seneca ZE-SG3 device.

        Returns:
            str: The password as a string.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.PASSWORD, count=1)

        if result.isError():
            print("Failed to retrieve password.")
            return None
        else:
            # get the 16-bit integer from the registers
            password = result.registers[0]
            return password
        

    def set_command_register(self, command):
        """
        Sets the command register on the Seneca ZE-SG3 device.

        Args:
            command (int): The command to set.

        Returns:
            None
        """

        print(command_register.__dict__.values())

        if command not in command_register.__dict__.values():
            print("Invalid command.")
            return None
        

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.COMMAND_REGISTER, command)

        if result.isError():
            print("Failed to set command register.")
        else:
            print("Command register set successfully.")


    def get_command_register(self):
        """
        Retrieves the command register from the Seneca ZE-SG3 device.

        Returns:
            str: The command register as a string.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.COMMAND_REGISTER, count=1)

        if result.isError():
            print("Failed to retrieve command register.")
            return None
        else:
            # get the 16-bit integer from the registers
            command = result.registers[0]
            return command


    def get_pieces_counter_value(self):
        """
        Retrieves the pieces counter value from the Seneca ZE-SG3 device.

        Returns:
            str: The pieces counter value as an integer.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.PIECES_NR, count=1)

        if result.isError():
            print("Failed to retrieve pieces counter value.")
            return None
        else:
            # get the 16-bit integer from the registers
            pieces_counter_value = result.registers[0]
            return pieces_counter_value


    def get_max_net_weight(self):
        """
        Retrieves the max net weight value from the Seneca ZE-SG3 device.

        Returns:
            str: The max net weight value as a float32.
        """
        # Replace with the actual register address and quantity
        
        result = self.client.read_holding_registers(register.MAX_NET_WEIGHT_MSW, count=2)

        if result.isError():
            print("Failed to retrieve max net weight value.")
            return None
        else:
            # get the 16-bit integer from the registers
            max_net_weight_msw = result.registers[0]
            max_net_weight_lsw = result.registers[1]
            return self._hex_to_float32((max_net_weight_msw << 16) + max_net_weight_lsw)

    def get_min_net_weight(self):
        """
        Retrieves the min net weight value from the Seneca ZE-SG3 device.

        Returns:
            str: The min net weight value as a float32.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.MIN_NET_WEIGHT_MSW, count=2)

        if result.isError():
            print("Failed to retrieve min net weight value.")
            return None
        else:
            # get the 16-bit integer from the registers
            min_net_weight_msw = result.registers[0]
            min_net_weight_lsw = result.registers[1]
            return self._hex_to_float32((min_net_weight_msw << 16) + min_net_weight_lsw)



    def get_adc_raw_24bit(self):
        """
        Retrieves the raw ADC value from the Seneca ZE-SG3 device.

        Returns:
            str: The raw ADC value as a 24-bit integer.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.ADC_RAW_24BIT_MSW, 2)

        if result.isError():
            print("Failed to retrieve raw ADC value.")
            return None
        else:
            # Combine the two 16-bit registers into a 32-bit integer
            msw = result.registers[0]
            lsw = result.registers[1]
            adc_raw_24bit = (msw << 16) | lsw

            return adc_raw_24bit


    def get_adc_filtered_24bit(self):
        """
        Retrieves the filtered ADC value from the Seneca ZE-SG3 device.

        Returns:
            str: The filtered ADC value as a 24-bit integer.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.ADC_FILTERED_24BIT_MSW, count=2)

        if result.isError():
            print("Failed to retrieve filtered ADC value.")
            return None
        else:
            # Combine the two 16-bit registers into a 32-bit integer
            msw = result.registers[0]
            lsw = result.registers[1]
            adc_filtered_24bit = (msw << 16) | lsw

            return adc_filtered_24bit
        


    def set_modbus_manual_analog_output(self, value_u32):
        """
        Sets the modbus manual analog output on the Seneca ZE-SG3 device.

        Args:
            value_u32 (int): The modbus manual analog output to set.

        Returns:
            None
        """
        modbus_manual_analog_output_msw = value_u32 >> 16
        modbus_manual_analog_output_lsw = value_u32 & 0xFFFF

        # Replace with the actual register address and quantity
        result = self.client.write_register(register.MODBUS_MANUAL_ANALOG_OUTPUT_MSW, modbus_manual_analog_output_msw)
        result = self.client.write_register(register.MODBUS_MANUAL_ANALOG_OUTPUT_LSW, modbus_manual_analog_output_lsw)

        if result.isError():
            print("Failed to set modbus manual analog output.")
        else:
            print("Modbus manual analog output set successfully.")


    def get_modbus_manual_analog_output(self):
        """
        Retrieves the modbus manual analog output from the Seneca ZE-SG3 device.

        Returns:
            str: The modbus manual analog output as a 32-bit integer.
        """
        # Replace with the actual register address and quantity
        result = self.client.read_holding_registers(register.MODBUS_MANUAL_ANALOG_OUTPUT_MSW, count=2)

        if result.isError():
            print("Failed to retrieve modbus manual analog output.")
            return None
        else:
            # get the 16-bit integer from the registers
            modbus_manual_analog_output_msw = result.registers[0]
            modbus_manual_analog_output_lsw = result.registers[1]
            return (modbus_manual_analog_output_msw << 16) + modbus_manual_analog_output_lsw




    def _float32_to_hex(self, value):
        """
        Converts a float to its hexadecimal representation.

        Args:
            value (float): The float value to convert.

        Returns:
            str: The hexadecimal representation of the float.
        """
        packed_value = struct.pack('!f', value)  # Pack the float as a binary string
        hex_value = packed_value.hex()           # Convert the binary string to a hex string
        return hex_value
    

    def _hex_to_float32(self, hex_value):
        """
        Converts a hexadecimal value back to its float32 representation.

        Args:
            hex_value (int): The hexadecimal value to convert (e.g., 0x42f6e979).

        Returns:
            float: The float32 representation of the hexadecimal value.
        """
        # Ensure the input is an integer (hexadecimal format)
        if isinstance(hex_value, str):
            hex_value = int(hex_value, 16)
        
        # Convert the integer to a 4-byte binary string
        packed_value = struct.pack('!I', hex_value)
        
        # Unpack the bytes as a float
        float_value = struct.unpack('!f', packed_value)[0]
        
        return float_value





# Example usage
# ze_sg3 = ZESG3()
# ze_sg3.open_server("192.168.0.101", 502)
# print(ze_sg3.get_machine_id())
# print(ze_sg3.get_firmware_version())




# print(ze_sg3._float32_to_hex(2.54))
# print(ze_sg3._hex_to_float32('40228f5c'))


# status = ze_sg3.get_status()
# print(status)
# print(status['threshold_and_stable_weight_for_dido1'])


# ze_sg3.close_server()
