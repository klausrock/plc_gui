# import nanotec_nanolib as nanolib
# import logging
# import httpx
from flask import Blueprint, request, jsonify
# from flask_login import login_required
# from app.models.stepperMotor import StepperMotor
# from app import os, db
# from app.utils.common import is_ip_alive
#
bp = Blueprint('self_test', __name__, url_prefix='/self_test')
#
# @bp.route('/device-id/<string:ip>', methods=['GET'])
# @login_required
# def get_device_id(ip):
#     try:
#         ip_address = ip
#
#         if not ip_address:
#             return jsonify({'error': 'ip_address required'}), 400
#
#     except Exception as e:
#         return jsonify({'error': str(e)})
#
# # Setup logging
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     handlers=[logging.FileHandler("motor_api.log"),
#                              logging.StreamHandler()])
# logger = logging.getLogger(__name__)
#
# class NanotecMotorHelper:
#     def __init__(self):
#         self.accessor = nanolib.NanoLibAccessor()
#         self.device_handle = None
#         self.bus_hardware_id = None
#
#     def list_available_hardware(self):
#         """List all available bus hardware."""
#         try:
#             result = self.accessor.listAvailableBusHardware()
#             if result.hasError():
#                 logger.error(f"Error listing hardware: {result.getError()}")
#                 return None
#             return result.getResult()
#         except Exception as e:
#             logger.error(f"Exception listing hardware: {str(e)}")
#             return None
#
#     def connect_to_hardware(self, bus_hw_id, options=None):
#         """Connect to specified bus hardware."""
#         try:
#             if options is None:
#                 options = nanolib.BusHardwareOptions()
#                 # For Ethernet connection
#                 options.addOption("RESTful Connect Timeout", "1000")
#                 options.addOption("RESTful Request Timeout", "1000")
#                 options.addOption("RESTful Response Timeout", "2000")
#
#             result = self.accessor.openBusHardwareWithProtocol(bus_hw_id, options)
#             if result.hasError():
#                 logger.error(f"Error connecting to hardware: {result.getError()}")
#                 return False
#
#             self.bus_hardware_id = bus_hw_id
#             return True
#         except Exception as e:
#             logger.error(f"Exception connecting to hardware: {str(e)}")
#             return False
#
#     def scan_for_devices(self):
#         """Scan for connected devices."""
#         try:
#             if not self.bus_hardware_id:
#                 logger.error("No bus hardware connected")
#                 return None
#
#             result = self.accessor.scanDevices(self.bus_hardware_id, None)
#             if result.hasError():
#                 logger.error(f"Error scanning devices: {result.getError()}")
#                 return None
#
#             return result.getResult()
#         except Exception as e:
#             logger.error(f"Exception scanning devices: {str(e)}")
#             return None
#
#     def connect_to_device(self, device_id):
#         """Connect to a specific device."""
#         try:
#             # Add the device to NanoLib's internal list
#             result = self.accessor.addDevice(device_id)
#             if result.hasError():
#                 logger.error(f"Error adding device: {result.getError()}")
#                 return False
#
#             self.device_handle = result.getResult()
#
#             # Connect to the device
#             connect_result = self.accessor.connectDevice(self.device_handle)
#             if connect_result.hasError():
#                 logger.error(f"Error connecting to device: {connect_result.getError()}")
#                 return False
#
#             return True
#         except Exception as e:
#             logger.error(f"Exception connecting to device: {str(e)}")
#             return False
#
#     def stop_nanoj_program(self):
#         """Stop the NanoJ program (write 0 to object 0x2300:00)."""
#         try:
#             if not self.device_handle:
#                 logger.error("No device connected")
#                 return False
#
#             # Create OD index for NanoJ program control (0x2300:00)
#             od_index = nanolib.OdIndex(0x2300, 0x00)
#
#             # Write value 0 to stop the NanoJ program
#             result = self.accessor.writeNumber(self.device_handle, 0, od_index, 8)  # 8-bit value
#             if result.hasError():
#                 logger.error(f"Error stopping NanoJ program: {result.getError()}")
#                 return False
#
#             logger.info("NanoJ program stopped successfully")
#             return True
#         except Exception as e:
#             logger.error(f"Exception stopping NanoJ program: {str(e)}")
#             return False
#
#     def read_object_value(self, index, subindex):
#         """Read a value from the object dictionary."""
#         try:
#             if not self.device_handle:
#                 logger.error("No device connected")
#                 return None
#
#             od_index = nanolib.OdIndex(index, subindex)
#             result = self.accessor.readNumber(self.device_handle, od_index)
#             if result.hasError():
#                 logger.error(f"Error reading object {hex(index)}:{hex(subindex)}: {result.getError()}")
#                 return None
#
#             return result.getResult()
#         except Exception as e:
#             logger.error(f"Exception reading object: {str(e)}")
#             return None
#
#     def write_object_value(self, index, subindex, value, bit_length=32):
#         """Write a value to the object dictionary."""
#         try:
#             if not self.device_handle:
#                 logger.error("No device connected")
#                 return False
#
#             od_index = nanolib.OdIndex(index, subindex)
#             result = self.accessor.writeNumber(self.device_handle, value, od_index, bit_length)
#             if result.hasError():
#                 logger.error(f"Error writing to object {hex(index)}:{hex(subindex)}: {result.getError()}")
#                 return False
#
#             return True
#         except Exception as e:
#             logger.error(f"Exception writing to object: {str(e)}")
#             return False
#
#     def disconnect_device(self):
#         """Disconnect from the device."""
#         try:
#             if not self.device_handle:
#                 return True  # Already disconnected
#
#             result = self.accessor.disconnectDevice(self.device_handle)
#             if result.hasError():
#                 logger.error(f"Error disconnecting device: {result.getError()}")
#                 return False
#
#             remove_result = self.accessor.removeDevice(self.device_handle)
#             if remove_result.hasError():
#                 logger.error(f"Error removing device: {remove_result.getError()}")
#                 return False
#
#             self.device_handle = None
#             return True
#         except Exception as e:
#             logger.error(f"Exception disconnecting device: {str(e)}")
#             return False
#
#     def disconnect_hardware(self):
#         """Disconnect from the bus hardware."""
#         try:
#             if not self.bus_hardware_id:
#                 return True  # Already disconnected
#
#             result = self.accessor.closeBusHardware(self.bus_hardware_id)
#             if result.hasError():
#                 logger.error(f"Error disconnecting hardware: {result.getError()}")
#                 return False
#
#             self.bus_hardware_id = None
#             return True
#         except Exception as e:
#             logger.error(f"Exception disconnecting hardware: {str(e)}")
#             return False
#
#     def cleanup(self):
#         """Cleanup all connections."""
#         self.disconnect_device()
#         self.disconnect_hardware()