Understanding thumbstick deadzones
==================================

What's this?
------------

Gamepads and similar thumbstick controllers usually give an input value between -1 and 1 in two axis. Thus, when the stick is idle the expected value is (0, 0). However, most of times the given value is near but not equal to 0. The idea of deadzone is like a threshold value for thumbstick input. Although it seems pretty simple, it can lead us into trouble if we don't implement it carefully.

This work is an extension of [this great article](http://www.third-helix.com/2013/04/12/doing-thumbstick-dead-zones-right.html) by Josh Sutphin. Here I'll go through different approaches for implementing deadzones, along with a playable demo. I hope this helps someone to choose the right one for her project.

I recommend to open the demo in another tab and do some tests while reading this document. Source code can be found in the "demo" folder (powered by the [Phaser engine](https://phaser.io/)). Also, in the file "main.py" you can find the program I used to generate all the images below (powered by [OpenCV](https://opencv.org/)).

Deadzone types
--------------

** !!! Article under construction !!! **

First I will explain how to interpret the graphs. We will be working with two types of graphs, both of them represent all possible values of some thumbstick input. Each pixel on the image corresponds to a single position of the stick.

- Grayscale: normalized magnitude of input vector (black = 0; white = 1).
	Variables: thumbstick raw input (x): pixel x coord
               thumbstick raw input (y): pixel y coord
			   thumbstick processed input (vector magnitude): gray value
			   (show with an image where are 0 and 1 values for every variable)
- RGB: normalized axis value of input vector (red for X axis, blue for Y axis)
	Variables: thumbstick raw input (x): pixel x coord
               thumbstick raw input (y): pixel y coord
			   thumbstick processed input (x): red value
			   thumbstick processed input (y): blue value
			   (show with an image where are 0 and 1 values for every variable)

Now I will discuss deadzone types. For each type, a graph and some python-ish pseudocode will be provided. First of all, if we don't apply a deadzone, our raw input magnitude graph will look like this:

![thumbstick graph - no deadzone][dz_none_gray]

Open the demo and move around a bit, then release the stick. You'll see how the character moves slightly although there's no user input anymore. That's what we want to solve by applying a deadzone function to the raw input. We'll try first the simplest approach: axial deadzone.

![thumbstick graph - axial][dz_axial_gray]

```python
def dz_axial(stick_input, deadzone):
	result = Vector2(stick_input)
	if (abs(result.x) < deadzone)
		result.x = 0
	if (abs(result.y) < deadzone)
		result.y = 0
	return result
```

This deadzone type causes kind of a "snap to grid" effect, very uncomfortable for 3D environments. At the demo, try to perform a slow circular motion, and you will notice this issue. So here is the next step, radial deadzone:

![thumbstick graph - radial][dz_radial_gray]

```python
def dz_radial(stick_input, deadzone):
	input_magnitude = get_magnitude(stick_input)
	if input_magnitude < deadzone:
		return Vector2(0, 0)
	else:
		return Vector2(stick_input)
```

But with this deadzone type there is another issue: we lose precision on the process. We're no longer getting input between -1 and 1, but rather in the [-1, -deadzone] and [deadzone, 1] intervals. If by clamping input we lose precision, then we don't should clamp, but rather *scale* input. We want to turn that sharp black edge into a smooth transition. In order to do that, I'm using a function that takes a value from an input range and returns its equivalent in the specified output range:

```python
def map_range(value, old_min, old_max, new_min, new_max):
	return (new_min + (new_max - new_min) * (value - old_min) / (old_max - old_min))
```

Then, we have our scaled radial deadzone:

![thumbstick graph - scaled radial][dz_scaled_radial_gray]

```python
def dz_scaled_radial(stick_input, deadzone):
	input_magnitude = get_magnitude(stick_input)
	if input_magnitude < deadzone:
		return Vector2(0, 0)
	else:
		input_normalized = stick_input / input_magnitude
		result = input_normalized * map_range(input_magnitude, deadzone, 1, 0, 1)
		return result
```

Now try the slowest movement you can perform with both radial and scaled radial deadzones. You will notice that with the scaled radial you have a wider speed range, in particular at low speeds. The transition from stillnes to movement is much smoother with scaled radial.

Ideally, this would be the deadzone that fits every project's needs. Unfortunately, this is not true. Sometimes we don't want the same amount of deadzone along an axis. At the demo, select the scaled radial deadzone and try to follow one of the horizontal blue lines at high speed. It's possible, but far from easy to get a pure horizontal motion (i.e. motion in X axis only). Look at the bottom left corner of the screen and try to get a 0 on the second axis. Many applications that work with analog input need at the same time to help the user to perform pure horizontal/vertical motion. So for this environments we need a special deadzone type.

How could we accomplish this? Well, one step at a time. We know that

1. Axial deadzone is good for pure horizontal/vertical motion (high input values)
2. Axial deadzone is bad for

All this leads us to the conclusion that we need a variable deadzone instead of a constant value. Like an axial deadzone function but with some slope in the edges, so that the deadzone is pretty low near the center and it constantly increases its value along the axis.

![thumbstick graph - sloped axial][dz_sloped_axial_gray]

```python
def dz_sloped_axial(stick_input, deadzone):
    deadzone_x = deadzone * abs(stick_input.y)
    deadzone_y = deadzone * abs(stick_input.x)
	result = Vector2(stick_input)
	if (abs(result.x) < deadzone_x)
		result.x = 0
	if (abs(result.y) < deadzone_y)
		result.y = 0
	return result
```

In the sample code you can see that now deadzone is split in two values (one for each axis). Note also that the deadzone amount for X axis depends on the current Y value, and vice versa.

Previously we have learned that is not a good thing to see edges on the graph. Edges mean sudden changes in motion, gradients mean smooth transitions. So, like we've done with radial deadzone, we may now *scale* the sloped axial in order to get rid of edges.

![thumbstick graph - sloped scaled axial][dz_sloped_scaled_axial_rgb]

```python
def dz_sloped_scaled_axial(stick_input, deadzone):
    deadzone_x = deadzone * abs(stick_input.y)
    deadzone_y = deadzone * abs(stick_input.x)
	result = Vector2(0, 0)
	sign = Vector2(get_sign(stick_input.x), get_sign(stick_input.y))
	if (abs(stick_input.x) > deadzone_x)
		result.x = sign.x * map_range(abs(stick_input.x), deadzone_x, 1, 0, 1)
	if (abs(stick_input.y) > deadzone_y)
		result.y = sign.y * map_range(abs(stick_input.y), deadzone_y, 1, 0, 1)
	return result
```

Now we shall combine this function with the scaled radial in order to avoid undesired input when the stick is released:

![thumbstick graph - hybrid][dz_hybrid_rgb]

```python
def dz_hybrid(stick_input, deadzone):
	input_magnitude = get_magnitude(stick_input)
    if input_magnitude < deadzone:
        return Vector2(0, 0)

    partial_output = dz_scaled_radial(stick_input, deadzone)

    final_output = dz_sloped_scaled_axial(partial_output, deadzone)

    return final_output
```

Note that the order in which the transformations are applied is relevant: scaled radial function must be called first in order to avoid distortion for low input values.

Testing
-------

Useful tests for the demo:
1. Do not touch the stick. Does the character stand still?

2. Try to perform a really soft acceleration. Is the transition from stillness to movement sudden or smooth?

3. Is it possible to perform a slow horizontal/vertical motion with a soft slope? Or does it feel like there are only 3 directions (horizontal/vertical/diagonal)?

4. Is it easy to perform a pure horizontal/vertical motion?

5. Test how easy is to do the following: align character's feet with one of the deep blue horizontal lines' edge; after that, move along that edge for a couple of seconds; then start to move slowly towards the other edge of the line; when you've reached it, keep moving along that edge for another two seconds. You can do this test at various speeds.

6. With the right stick perform a circular motion at a constant angular speed. Does the character rotate smoothly? Or does he seem to "stop" for a moment at certain rotations (specifically when X=0 or Y=0)?

I've been doing some testing with both Xbox 360 and PS3 official controllers (Debian + Firefox environment), and I've found something quite interesting: with PS3 controller there's no need to do deadzone processing at all. It works reeeally smooth in every case... with deadzone set to *None*! One may think that it could be just an excellent piece of hardware and no post-processing is needed. But test #6 reveals something against this hypothesis: it "stops" at certain positions, very similar to our hybrid deadzone behavior. That's a clear proof of a deadzone post-process running beneath the surface. Does the PS3 controller have kind of a built-in deadzone? Or is it the linux driver? No idea. So, please, if you can throw some light on this issue, I'd really appreciate it. I've also tested the Dualshock in Cocos2D engine with identical result.

Well, so below you can see the results table for these tests that I've run. You can reproduce them in the demo. Also, I'm looking forward to test Xbox ONE controller as soon as possible.

|  | 1 | 2 | 3 | 4 | 5 | 6 |
|--|---|---|---|---|---|---|
| Axial | | | | | | |
| Radial |
| Hybrid |
| PS3? |

Final notes
-----------
Well, that's all for now. I hope you've find it useful. If you have any thoughts, new ideas or corrections, feel free to fork this repo or to submit a pull request! Thanks for reading! :]

TODO
----
- Test more with PS3 controller
- Finish this document

License
-------

Copyright (C)  2017  Carlos Pérez Ramil.

Permission is granted to copy, distribute and/or modify this document under the terms of the GNU Free Documentation License, Version 1.3 or any later version published by the Free Software Foundation; with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts. A copy of the license is included in the file "fdl-1.3.txt".


[dz_none_gray]: demo/assets/image/dz_none_gray.png "No deadzone"
[dz_none_rgb]: demo/assets/image/dz_none_rgb.png "No deadzone"
[dz_axial_gray]: demo/assets/image/dz_axial_gray.png "Axial deadzone"
[dz_axial_x_gray]: demo/assets/image/dz_axial_x_gray.png "Axial deadzone (x axis)"
[dz_axial_y_gray]: demo/assets/image/dz_axial_y_gray.png "Axial deadzone (y axis)"
[dz_radial_gray]: demo/assets/image/dz_radial_gray.png "Radial deadzone"
[dz_scaled_axial_gray]: demo/assets/image/dz_scaled_axial_gray.png "Scaled axial deadzone"
[dz_scaled_radial_gray]: demo/assets/image/dz_scaled_radial_gray.png "Scaled radial deadzone"
[dz_sloped_axial_gray]: demo/assets/image/dz_sloped_axial_gray.png "Sloped axial deadzone"
[dz_sloped_axial_rgb]: demo/assets/image/dz_sloped_axial_rgb.png "Sloped axial deadzone"
[dz_sloped_scaled_axial_rgb]: demo/assets/image/dz_sloped_scaled_axial_rgb.png "Sloped scaled axial deadzone"
[dz_hybrid_rgb]: demo/assets/image/dz_hybrid_rgb.png "Hybrid deadzone"
