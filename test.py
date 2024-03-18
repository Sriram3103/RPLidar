# import pyrplidar

# # Connect to the RPLidar sensorlidar = PyRPlidar()
# lidar = PyRPLidar()
# lidar.connect(port="C0", baudrate=256000, timeout=3)
# info = lidar.get_info()
# print(f"RPLidar Info: {info}")

# # Start scanning
# lidar.start_scanning()

# try:
#   while True:
#     # Get a scan measurement
#     response = lidar.get_measurement()[0]
#     distance = response[2]
#     quality = response[3]

#     # Print distance and quality
#     print(f"Distance: {distance} mm, Quality: {quality}")

# except KeyboardInterrupt:
#   # Stop scanning on keyboard interrupt
#   lidar.stop_scanning()
#   print("Scanning stopped.")

# finally:
#   # Disconnect from the sensor
#   lidar.disconnect()
#   print("Disconnected from RPLidar.")
from pyrplidar import PyRPlidar

lidar = PyRPlidar()
lidar.connect(port="COM3", baudrate=9600, timeout=1)
# Linux   : "/dev/ttyUSB0"
# MacOS   : "/dev/cu.SLAB_USBtoUART"
# Windows : "COM5"


info = lidar.get_info()
print("info :", info)

health = lidar.get_health()
print("health :", health)

samplerate = lidar.get_samplerate()
print("samplerate :", samplerate)


scan_modes = lidar.get_scan_modes()
print("scan modes :")
for scan_mode in scan_modes:
    print(scan_mode)


lidar.disconnect()