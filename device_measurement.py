# #!/usr/bin/env python3

# from datetime import datetime
# from os import path
# import csv
# from rplidar import RPLidar

# BAUDRATE: int = 115200
# TIMEOUT: int = 1

# output_filename = 'lid1.csv'

# def run():
#     raw = True
#     lidar = RPLidar(port='COM3', baudrate=BAUDRATE, timeout=TIMEOUT)
#     try:

#         if not raw:
#             print('Print measurements - Press Crl+C to stop.')
#             now = datetime.now()
#             date_time = now.strftime("%d/%m/%Y %H:%M:%S")
#             print('Date & Time  : {0}'.format(date_time))
#         with open(output_filename, 'w', newline='') as csvfile:  # Open CSV file in write mode (newline='') for compatibility
#             csv_writer = csv.writer(csvfile)
#             for val in lidar.iter_scans():
#                 for i in val:
#                     csv_writer.writerow([i[2], i[0]]) 
#                     print(i[0],i[1],i[2])
#                 break
#         lidar.stop()
#         lidar.stop_motor()
#         lidar.disconnect()
#     except KeyboardInterrupt:
#         lidar.stop()
#         lidar.stop_motor()
#         lidar.disconnect()
# if __name__ == '__main__':
#     run()
#!/usr/bin/env python3

from datetime import datetime
from os import path
import csv
from rplidar import RPLidar
from convert import convert_angles
from plot import ploting



BAUDRATE: int = 115200
TIMEOUT: int = 1

output_filename = 'lid2.csv'
def run():
    print('running')
    count = 0
    raw = True
    lidar = RPLidar(port='COM3', baudrate=BAUDRATE, timeout=TIMEOUT)
    try:

        if not raw:
            print('Print measurements - Press Crl+C to stop.')
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            print('Date & Time  : {0}'.format(date_time))
        with open(output_filename, 'w', newline='') as csvfile:  # Open CSV file in write mode (newline='') for compatibility
            csv_writer = csv.writer(csvfile)
            for val in lidar.iter_scans():
                for i in val:
                    csv_writer.writerow([i[2], i[1]]) 
                    print(i[0],i[1],i[2])
                count+=1
                if count==8:
                    break
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
    except KeyboardInterrupt:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
if __name__ == '__main__':
    run()
    convert_angles('lid2.csv', 'lid3.csv')
    ploting()
# for i in range(10):
#     run()
    