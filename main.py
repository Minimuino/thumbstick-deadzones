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

TAU = 2 * np.pi

# UTILS
def map_range(v, old_min, old_max, new_min, new_max):
    return (new_min + (new_max - new_min) * (v - old_min) / (old_max - old_min))


# DEADZONE TYPES
def dz_none(stick_input, deadzone):
    return stick_input[0], stick_input[1]

def dz_axial_x(stick_input, deadzone):
    x_val = stick_input[0] if abs(stick_input[0]) > deadzone else 0
    return x_val, 0

def dz_axial_y(stick_input, deadzone):
    y_val = stick_input[1] if abs(stick_input[1]) > deadzone else 0
    return 0, y_val

def dz_axial(stick_input, deadzone):
    x_val = stick_input[0] if abs(stick_input[0]) > deadzone else 0
    y_val = stick_input[1] if abs(stick_input[1]) > deadzone else 0
    return x_val, y_val

def dz_sloped_axial_x(stick_input, deadzone):
    deadzone_x = deadzone * abs(stick_input[1])
    x_val = stick_input[0] if abs(stick_input[0]) > deadzone_x else 0
    return x_val, 0

def dz_sloped_axial_y(stick_input, deadzone):
    deadzone_y = deadzone * abs(stick_input[0])
    y_val = stick_input[1] if abs(stick_input[1]) > deadzone_y else 0
    return 0, y_val

def dz_sloped_axial(stick_input, deadzone):
    deadzone_x = deadzone * abs(stick_input[1])
    deadzone_y = deadzone * abs(stick_input[0])
    x_val = stick_input[0] if abs(stick_input[0]) > deadzone_x else 0
    y_val = stick_input[1] if abs(stick_input[1]) > deadzone_y else 0
    return x_val, y_val

def dz_radial(stick_input, deadzone):
    input_magnitude = np.linalg.norm(stick_input)
    if input_magnitude < deadzone:
        return 0, 0
    else:
        return stick_input[0], stick_input[1]

def dz_scaled_axial_x(stick_input, deadzone):
    x_val = 0
    sign = np.sign(stick_input[0])
    if abs(stick_input[0]) > deadzone:
        x_val = sign * map_range(abs(stick_input[0]), deadzone, 1, 0, 1)
    return x_val, 0

def dz_scaled_axial_y(stick_input, deadzone):
    y_val = 0
    sign = np.sign(stick_input[1])
    if abs(stick_input[1]) > deadzone:
        y_val = sign * map_range(abs(stick_input[1]), deadzone, 1, 0, 1)
    return 0, y_val

def dz_scaled_axial(stick_input, deadzone):
    x_val = 0
    y_val = 0
    sign = np.sign(stick_input)
    if abs(stick_input[0]) > deadzone:
        x_val = sign[0] * map_range(abs(stick_input[0]), deadzone, 1, 0, 1)
    if abs(stick_input[1]) > deadzone:
        y_val = sign[1] * map_range(abs(stick_input[1]), deadzone, 1, 0, 1)
    return x_val, y_val

def dz_sloped_scaled_axial_x(stick_input, deadzone):
    x_val = 0
    deadzone_x = deadzone * abs(stick_input[1])
    sign = np.sign(stick_input[0])
    if abs(stick_input[0]) > deadzone_x:
        x_val = sign * map_range(abs(stick_input[0]), deadzone_x, 1, 0, 1)
    return x_val, 0

def dz_sloped_scaled_axial_y(stick_input, deadzone):
    y_val = 0
    deadzone_y = deadzone * abs(stick_input[0])
    sign = np.sign(stick_input[1])
    if abs(stick_input[1]) > deadzone_y:
        y_val = sign * map_range(abs(stick_input[1]), deadzone_y, 1, 0, 1)
    return 0, y_val

def dz_sloped_scaled_axial(stick_input, deadzone, n=1):
    x_val = 0
    y_val = 0
    deadzone_x = deadzone * np.power(abs(stick_input[1]), n)
    deadzone_y = deadzone * np.power(abs(stick_input[0]), n)
    sign = np.sign(stick_input)
    if abs(stick_input[0]) > deadzone_x:
        x_val = sign[0] * map_range(abs(stick_input[0]), deadzone_x, 1, 0, 1)
    if abs(stick_input[1]) > deadzone_y:
        y_val = sign[1] * map_range(abs(stick_input[1]), deadzone_y, 1, 0, 1)
    return x_val, y_val

def dz_scaled_radial(stick_input, deadzone):
    input_magnitude = np.linalg.norm(stick_input)
    if input_magnitude < deadzone:
        return 0, 0
    else:
        input_normalized = stick_input / input_magnitude
        # Formula:
        # max_value = 1
        # min_value = 0
        # retval = input_normalized * (min_value + (max_value - min_value) * ((input_magnitude - deadzone) / (max_value - deadzone)))
        retval = input_normalized * map_range(input_magnitude, deadzone, 1, 0, 1)
        return retval[0], retval[1]

def dz_hybrid(stick_input, deadzone):
    # First, check that input does not fall within deadzone
    input_magnitude = np.linalg.norm(stick_input)
    if input_magnitude < deadzone:
        return 0, 0

    # Then apply a scaled_radial transformation
    partial_output = dz_scaled_radial(stick_input, deadzone)

    # Then apply a sloped_scaled_axial transformation
    final_output = dz_sloped_scaled_axial(partial_output, deadzone)

    return final_output

def dz_exp(stick_input, deadzone, n=3):
    partial_output = dz_scaled_radial(stick_input, deadzone)
    input_magnitude = np.linalg.norm(partial_output)
    if input_magnitude == 0:
        return 0, 0
    input_normalized = partial_output / input_magnitude
    return input_normalized * np.power(input_magnitude, n)

def dz_scaled_radial_inner_and_outer(stick_input, inner_deadzone, outer_deadzone=0.15):
    input_magnitude = np.linalg.norm(stick_input)
    if input_magnitude < inner_deadzone:
        return 0, 0
    elif input_magnitude > (1 - outer_deadzone):
        return stick_input / input_magnitude
    else:
        input_normalized = stick_input / input_magnitude
        retval = input_normalized * map_range(input_magnitude, inner_deadzone, 1 - outer_deadzone, 0, 1)
        return retval[0], retval[1]

def directional_adjustment(stick_input, target_direction, angle_range=np.pi/4):
    input_magnitude = np.linalg.norm(stick_input)
    if input_magnitude == 0:
        return 0, 0

    target_direction_normalized = target_direction / np.linalg.norm(target_direction)

    # Find out the angles of the vectors in the [-pi, pi] range
    input_angle = np.arctan2(stick_input[1], stick_input[0])
    target_direction_angle = np.arctan2(target_direction[1], target_direction[0])

    # Apply directional adjustment if the input falls within the zone delimited by target_direction and angle_range
    angle_diff = find_shortest_angle_diff(input_angle, target_direction_angle)
    if abs(angle_diff) < angle_range:
        return np.array(target_direction_normalized) * input_magnitude

    # Shrink all values out of adjustment zone
    # First calculate the limits of the adjustment zone
    adjustment_zone_bottom = keep_angle_in_minuspi_pi_interval(target_direction_angle - angle_range)
    adjustment_zone_top = keep_angle_in_minuspi_pi_interval(target_direction_angle + angle_range)

    # Now calculate the new angle by using a discontinuous linear mapping function
    new_angle = target_direction_angle
    if adjustment_zone_bottom >= adjustment_zone_top:
        new_angle = line_equation_from_two_points(input_angle, (-np.pi + angle_range, -np.pi), (np.pi - angle_range, np.pi))
    elif input_angle > adjustment_zone_top:
        new_angle = line_equation_from_two_points(input_angle, (adjustment_zone_top, target_direction_angle), (adjustment_zone_bottom + TAU, target_direction_angle + TAU))
    elif input_angle < adjustment_zone_bottom:
        new_angle = line_equation_from_two_points(input_angle, (adjustment_zone_top - TAU, target_direction_angle - TAU), (adjustment_zone_bottom, target_direction_angle))

    return np.array((np.cos(new_angle), np.sin(new_angle))) * input_magnitude

def find_shortest_angle_diff(input_angle, target_direction_angle):
    return keep_angle_in_minuspi_pi_interval(input_angle - target_direction_angle)

def keep_angle_in_minuspi_pi_interval(angle):
    if angle > np.pi:
        return angle -TAU
    elif angle < -np.pi:
        return angle + TAU
    else:
        return angle

def line_equation_from_two_points(x, p1, p2):
    return ((p2[1] - p1[1])/(p2[0] - p1[0]))*(x - p1[0]) + p1[1]

################################################################################

# INPUT PARAMETERS
height = 400
width  = 400
center = (height/2, width/2)
deadzone = 0.2
deadzone_function = dz_hybrid
mode = 'rgb'

def generate_gray_image():
    # Base blank image
    img = np.full((height, width), 0, np.uint8)

    # Draw gradient and deadzone
    for i in range(height):
        for j in range(width):
            # Simulate stick input
            fake_stick_input = np.array([j - center[1], i - center[0]], dtype=float)
            fake_stick_input /= (height / 2)
            # Clamp fake input to stick boundaries
            magnitude = np.linalg.norm(fake_stick_input)
            if magnitude > 1.0:
                img[i,j] = 0
            else:
                # Compute deadzoned value
                n, m = deadzone_function(fake_stick_input, deadzone)
                dz_magnitude = np.linalg.norm([n,m])
                img[i,j] = map_range(dz_magnitude, 0, 1, 0, 255)

    # Print image
    plt.imshow(img, cmap=plt.cm.gray, vmin=0, vmax=255,
               aspect='equal', interpolation='bilinear')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.gca().invert_yaxis()
    plt.show()

    return img

def generate_rgb_image():
    # Base blank image
    img = np.full((height, width, 3), 0, np.uint8)

    # Draw gradient and deadzone
    for i in range(height):
        for j in range(width):
            # Simulate stick input
            fake_stick_input = np.array([j - center[1], i - center[0]], dtype=float)
            fake_stick_input /= (height / 2)
            # Clamp fake input to stick boundaries
            magnitude = np.linalg.norm(fake_stick_input)
            if magnitude > 1.0:
                img[i,j,0] = 0
            else:
                # Compute deadzoned value
                n, m = deadzone_function(fake_stick_input, deadzone)
                img[i,j,0] = map_range(abs(m), 0, 1, 0, 255)
                img[i,j,2] = map_range(abs(n), 0, 1, 0, 255)

    # Print image
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB), vmin=0, vmax=255,
               aspect='equal', interpolation='bilinear')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.gca().invert_yaxis()
    plt.show()

    return img

def main():

    img = None
    if mode == 'gray':
        img = generate_gray_image()
    elif mode == 'rgb':
        img = generate_rgb_image()

    # Listen for input
    command = input()
    if command == 's':
        print("File name: ")
        filename = input()
        cv.imwrite(filename, img)

if __name__ == '__main__':

    main()
