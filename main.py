# -*- coding: utf-8 -*-

# Copyright (C) 2017 Carlos Pérez Ramil

# This file is part of Thumbstick Deadzones project.

# The Thumbstick Deadzones project is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# The Thumbstick Deadzones project is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with the Thumbstick Deadzones project.
# If not, see <http://www.gnu.org/licenses/>.

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance as dist


# UTILS
def map_range(v, (old_min, old_max, new_min, new_max)):
    return (new_min + (new_max - new_min) * (v - old_min) / (old_max - old_min))


# DEADZONE TYPES
def dz_none(stick_input, deadzone):
    return stick_input[0], stick_input[1]

def dz_axial(stick_input, deadzone):
    x_val = stick_input[0] if abs(stick_input[0]) > deadzone else 0
    y_val = stick_input[1] if abs(stick_input[1]) > deadzone else 0
    return x_val, y_val

def dz_axial_x(stick_input, deadzone):
    x_val = stick_input[0] if abs(stick_input[0]) > deadzone else 0
    return x_val, 0

def dz_axial_y(stick_input, deadzone):
    y_val = stick_input[1] if abs(stick_input[1]) > deadzone else 0
    return 0, y_val

def dz_radial(stick_input, deadzone):
    input_magnitude = np.linalg.norm(stick_input)
    if input_magnitude < deadzone:
        return 0, 0
    else:
        return stick_input[0], stick_input[1]

def dz_scaled_axial_x(stick_input, deadzone):
    max_value = 1
    x_val = 0
    sign = np.sign(stick_input[0])
    if abs(stick_input[0]) > deadzone:
        x_val = sign * map_range(abs(stick_input[0]), (deadzone, max_value, 0, max_value))
    return x_val, 0

def dz_scaled_axial_y(stick_input, deadzone):
    max_value = 1
    y_val = 0
    sign = np.sign(stick_input[1])
    if abs(stick_input[1]) > deadzone:
        y_val = sign * map_range(abs(stick_input[1]), (deadzone, max_value, 0, max_value))
    return 0, y_val

def dz_scaled_axial(stick_input, deadzone):
    max_value = 1
    x_val = 0
    y_val = 0
    sign = np.sign(stick_input)
    if abs(stick_input[0]) > deadzone:
        x_val = sign[0] * map_range(abs(stick_input[0]), (deadzone, max_value, 0, max_value))
    if abs(stick_input[1]) > deadzone:
        y_val = sign[1] * map_range(abs(stick_input[1]), (deadzone, max_value, 0, max_value))
    return x_val, y_val

def dz_scaled_radial(stick_input, deadzone):
    max_value = 1
    min_value = 0
    input_magnitude = np.linalg.norm(stick_input)
    sign = np.sign(stick_input)
    if input_magnitude < deadzone:
        return 0, 0
    else:
        input_normalized = stick_input / input_magnitude
        retval = input_normalized * (min_value + (max_value - min_value) * ((input_magnitude - deadzone) / (max_value - deadzone)))
        # x_val = map_range(abs(stick_input[0]), (deadzone, max_value, 0, max_value))
        # y_val = map_range(abs(stick_input[1]), (deadzone, max_value, 0, max_value))
        # retval = [sign[0] * x_val, sign[1] * y_val]
        return retval[0], retval[1]

def dz_hybrid(stick_input, deadzone):
    pass

################################################################################

# INPUT PARAMETERS
height = 400
width  = 400
center = (height/2, width/2)
deadzone = 0.2
deadzone_function = dz_scaled_radial
mode = 'rgb'

def generate_gray_image():
    # Base blank image
    img = np.full((height, width), 0, np.uint8)

    # Draw gradient and deadzone
    for i in range(height):
        for j in range(width):
            # Simulate stick input
            fake_stick_input = np.array([j - center[1], i - center[0]], dtype=np.float)
            fake_stick_input /= (height / 2)
            # Clamp fake input to stick boundaries
            magnitude = np.linalg.norm(fake_stick_input)
            if magnitude > 1.0:
                img[i,j] = 0
            else:
                # Compute deadzoned value
                n, m = deadzone_function(fake_stick_input, deadzone)
                dz_magnitude = np.linalg.norm([n,m])
                img[i,j] = map_range(dz_magnitude, (0, 1, 0, 255))

    # Print image
    plt.imshow(img, cmap=plt.cm.gray, vmin=0, vmax=255,
               aspect='equal', interpolation='bilinear')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show(False)

def generate_rgb_image():
    # Base blank image
    img = np.full((height, width, 3), 0, np.uint8)

    # Draw gradient and deadzone
    for i in range(height):
        for j in range(width):
            # Simulate stick input
            fake_stick_input = np.array([j - center[1], i - center[0]], dtype=np.float)
            fake_stick_input /= (height / 2)
            # Clamp fake input to stick boundaries
            magnitude = np.linalg.norm(fake_stick_input)
            if magnitude > 1.0:
                img[i,j,0] = 0
            else:
                # Compute deadzoned value
                n, m = deadzone_function(fake_stick_input, deadzone)
                img[i,j,0] = map_range(abs(n), (0, 1, 0, 255))
                img[i,j,2] = map_range(abs(m), (0, 1, 0, 255))

    # Print image
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB), vmin=0, vmax=255,
               aspect='equal', interpolation='bilinear')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show(False)

def main():

    img = None
    if mode == 'gray':
        img = generate_gray_image()
    elif mode == 'rgb':
        img = generate_rgb_image()

    # Listen for input
    command = raw_input()
    if command == 's':
        print "File name: "
        filename = raw_input()
        cv.imwrite(filename, img)

if __name__ == '__main__':

    main()
