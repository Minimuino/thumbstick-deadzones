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
from matplotlib import animation

PI = np.pi
TAU = 2 * PI

# UTILS
def map_range(v, old_min, old_max, new_min, new_max):
    return (new_min + (new_max - new_min) * (v - old_min) / (old_max - old_min))

# DIRECTIONAL ADJUSTMENT FUNCTION
def directional_adjustment(stick_input, target_direction, angle_range=PI/4):
    input_magnitude = np.linalg.norm(stick_input)
    if input_magnitude == 0:
        return 0, 0

    # Find out the angles of the vectors in the [-pi, pi] range
    input_angle = np.arctan2(stick_input[1], stick_input[0])
    target_direction_angle = np.arctan2(target_direction[1], target_direction[0])

    # Apply directional adjustment if the input falls within the zone delimited by target_direction and angle_range
    angle_diff = keep_angle_in_minuspi_pi_interval(input_angle - target_direction_angle)
    if abs(angle_diff) < angle_range:
        target_direction_normalized = target_direction / np.linalg.norm(target_direction)
        return np.array(target_direction_normalized) * input_magnitude

    # Shrink all values out of adjustment zone
    # First calculate the limits of the adjustment zone (in radians)
    adjustment_zone_bottom = target_direction_angle - angle_range
    adjustment_zone_top = target_direction_angle + angle_range

    # Now calculate the new angle by using the line equation from two known points
    new_angle = target_direction_angle
    if input_angle > adjustment_zone_top:
        new_angle = line_equation_from_two_points(input_angle, (adjustment_zone_top, target_direction_angle),
                                                  (adjustment_zone_bottom + TAU, target_direction_angle + TAU))
    elif input_angle < adjustment_zone_bottom:
        new_angle = line_equation_from_two_points(input_angle, (adjustment_zone_top - TAU, target_direction_angle - TAU),
                                                  (adjustment_zone_bottom, target_direction_angle))

    return np.array((np.cos(new_angle), np.sin(new_angle))) * input_magnitude

def keep_angle_in_minuspi_pi_interval(angle):
    if angle > PI:
        return angle -TAU
    elif angle < -PI:
        return angle + TAU
    else:
        return angle

def line_equation_from_two_points(x, p1, p2):
    return ((p2[1] - p1[1])/(p2[0] - p1[0]))*(x - p1[0]) + p1[1]

# IMAGE GENERATION
def generate_rgb_image(height, width, direction, angle_range):
    # Base blank image
    img = np.full((height, width, 3), 0, np.uint8)
    center = (height/2, width/2)

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
                n, m = directional_adjustment(fake_stick_input, direction, angle_range)
                img[i,j,0] = map_range(abs(m), 0, 1, 0, 255)
                img[i,j,2] = map_range(abs(n), 0, 1, 0, 255)

    return img

def generate_animation(height, width, directions, angle_ranges, frames):
    fig = plt.figure()
    im = plt.imshow(cv.cvtColor(generate_rgb_image(height, width, directions[0], angle_ranges[0]), cv.COLOR_BGR2RGB),
                    vmin=0, vmax=255, aspect='equal', interpolation='bilinear')
    plt.gca().invert_yaxis()
    plt.xticks([]), plt.yticks([])

    def animate(i):
        a = cv.cvtColor(generate_rgb_image(height, width, directions[i], angle_ranges[i]), cv.COLOR_BGR2RGB)
        im.set_data(a)
        return [im]

    anim = animation.FuncAnimation(fig, animate, frames=frames, interval=40, blit=False)
    anim.save('basic_animation.mp4', extra_args=['-vcodec', 'libx264'])
    plt.show()

def generate_image(height, width, direction, angle_range):
    img = generate_rgb_image(height, width, direction, angle_range)
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB), vmin=0, vmax=255,
               aspect='equal', interpolation='bilinear')
    plt.xticks([]), plt.yticks([])
    plt.gca().invert_yaxis()
    plt.show()

    # Listen for input
    command = input()
    if command == 's':
        print("File name: ")
        filename = input()
        cv.imwrite(filename, cv.flip(img, 0))

if __name__ == '__main__':
    # INPUT PARAMETERS
    height = 400
    width  = 400
    constant_angle_range_params = {
        'frames': 16,
        'directions': np.vstack([np.linspace((-1, 0), (0, 1), 4, endpoint=False),
                            np.linspace((0, 1), (1, 0), 4, endpoint=False),
                            np.linspace((1, 0), (0, -1), 4, endpoint=False),
                            np.linspace((0, -1), (-1, 0), 4, endpoint=False)]),
        'angle_ranges': np.linspace(PI/4, PI/4, 16)
    }
    variable_angle_range_params = {
        'frames': 60,
        'directions': np.vstack([np.linspace((-1, 0), (-1, 0), 20, endpoint=False),
                              np.linspace((0, -1), (0, -1), 20, endpoint=False),
                              np.linspace((-1, -1), (-1, -1), 20, endpoint=False)]),
        'angle_ranges': np.vstack([np.linspace(0, PI/4, 10, endpoint=False),
                                       np.linspace(PI/4, 0, 10, endpoint=False),
                                       np.linspace(0, PI/4, 10, endpoint=False),
                                       np.linspace(PI/4, 0, 10, endpoint=False),
                                       np.linspace(0, PI/4, 10, endpoint=False),
                                       np.linspace(PI/4, 0, 10, endpoint=False)]).flatten()
    }

    # generate_image(height, width, (-1, -1), PI/4)
    generate_animation(height, width, variable_angle_range_params['directions'],
                       variable_angle_range_params['angle_ranges'],
                       variable_angle_range_params['frames'])
