import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import lidar_to_grid_map_dda as lg
from math import cos, sin, radians, pi
def ploting():
    def file_read(f):
        """
        Reading LIDAR laser beams (angles and corresponding distance data)
        """
        measures = [line.split(",") for line in open(f)]
        quality = []
        distances = []
        for measure in measures:
            quality.append(float(measure[1]))
            distances.append(float(measure[0]))
        quality = np.array(quality)
        distances = np.array(distances)
        return quality, distances

    # Open the CSV file for reading and writing
    with open('lid3.csv', 'r+', newline='') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        # Read the CSV data into a list of rows
        rows = list(reader)

        # Iterate through each row in the list
        for row in rows:
            # Convert the value in the second column to float and divide by 1000
            row[0] = str(float(row[0]) / 1000)

        # Move the file pointer to the beginning
        file.seek(0)
        # Create a CSV writer object
        writer = csv.writer(file)
        # Write each modified row to the file
        writer.writerows(rows)

        # If the new data is shorter than the old data, truncate the file to the new size
        file.truncate()
    xyreso = 0.015  # x-y grid resolution
    yawreso = math.radians(3.1)  # yaw angle resolution [rad]
    ang, dist = file_read("lid3.csv")
    ox = np.sin(ang) * dist
    oy = np.cos(ang) * dist
    pmap, minx, maxx, miny, maxy, xyreso = lg.generate_ray_casting_grid_map(ox, oy, xyreso, True)
    xyres = np.array(pmap).shape
    plt.figure(figsize=(20,8))
    plt.subplot(122)
    plt.imshow(pmap, cmap = "PiYG_r")
    plt.clim(-0.4, 1.4)
    plt.gca().set_xticks(np.arange(-.5, xyres[1], 1), minor = True)
    plt.gca().set_yticks(np.arange(-.5, xyres[0], 1), minor = True)
    plt.grid(True, which="minor", color="w", linewidth = .6, alpha = 0.5)
    plt.colorbar()
    plt.show()