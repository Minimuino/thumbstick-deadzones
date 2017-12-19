Understanding thumbstick deadzones
==================================

What's this?
------------

Gamepads and similar thumbstick controllers usually give an input value between -1 and 1 in two axis. Thus, when the stick is idle the expected value is (0, 0). However, most of times the given value is near but not equal to 0. The idea of deadzone is like a threshold value for thumbstick input. Although it seems pretty simple, it can lead us into trouble if we don't implement it carefully.

This work is an extension of [this great article](http://www.third-helix.com/2013/04/12/doing-thumbstick-dead-zones-right.html) by Josh Sutphin. Here I'll go through different approaches for implementing deadzones, along with a playable demo. I hope this helps someone to choose the right one for her project.

Deadzone types
--------------

# !!! Article under construction !!!

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

Now I will discuss deadzone types. If we don't apply a deadzone, our raw input magnitude graph will look like this:

![thumbstick graph - no deadzone][dz_none_gray]

We're now going to see how it looks with a simple axial deadzone:

![thumbstick graph - axial][dz_axial_gray]

This deadzone type causes kind of a "snap to grid" effect, very uncomfortable for 3D environments. At the demo, try to perform a slow circular movement, and you will notice this issue. So here is the next step: radial deadzone:

![thumbstick graph - radial][dz_radial_gray]

But with this deadzone type there is another issue: we lose precision on the process. Because of that, we should scale the range. In order to do that, I'm using a function that takes a value from an input range and returns its equivalent in the specified output range:

	def map_range(v, (old_min, old_max, new_min, new_max)):
		return (new_min + (new_max - new_min) * (v - old_min) / (old_max - old_min))

![thumbstick graph - scaled radial][dz_scaled_radial_gray]

Now try the slowest movement you can perform with both radial and scaled radial deadzones. You will notice that with the scaled radial you have a wider speed range, in particular at low speeds. The transition from stillnes to movement is much smoother with scaled radial.

Ideally, this would be the deadzone that fits every project's needs. Unfortunately, this is not true. Sometimes we don't want the same amount of deadzone along an axis. At the demo, select the scaled radial deadzone and try to follow one of the horizontal blue lines at high speed. It's possible, but not easy to get a pure horizontal movement (i.e. look at the bottom left corner of the screen and try to get a 0 on the second axis). Because of this, we need a new deadzone type:

![thumbstick graph - hybrid][dz_hybrid_rgb]

Useful tests for the [demo]():
1. Do not touch the stick. Does the character stand still?

2. Try to perform a really soft acceleration. Is the transition from stillness to movement sudden or smooth?

3. Is it possible to perform a slow horizontal/vertical movement with a small angle rotation? Or does it feel like there are only 3 directions (horizontal/vertical/diagonal)?

4. Is it easy to perform a pure horizontal/vertical movement?

5. Test how easy is to do the following: align character's feet with one of the deep blue horizontal lines' edge; after that, move along that edge for a couple of seconds; then start to move slowly towards the other edge of the line; when you've reached it, keep moving along that edge for another two seconds. You can do this test at various speeds.

License
-------

Copyright (C)  2017  Carlos Pérez Ramil.

Permission is granted to copy, distribute and/or modify this document under the terms of the GNU Free Documentation License, Version 1.3 or any later version published by the Free Software Foundation; with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts. A copy of the license is included in the file "fdl-1.3.txt".


[dz_none_gray]: demo/assets/image/dz_none_gray.png "No deadzone"
[dz_none_rgb]: demo/assets/image/dz_none_rgb.png "No deadzone"
[dz_axial_gray]: demo/assets/image/dz_axial_gray.png "No deadzone"
[dz_axial_x_gray]: demo/assets/image/dz_axial_x_gray.png "No deadzone"
[dz_axial_y_gray]: demo/assets/image/dz_axial_y_gray.png "No deadzone"
[dz_radial_gray]: demo/assets/image/dz_radial_gray.png "No deadzone"
[dz_scaled_axial_gray]: demo/assets/image/dz_scaled_axial_gray.png "No deadzone"
[dz_scaled_radial_gray]: demo/assets/image/dz_scaled_radial_gray.png "No deadzone"
[dz_hybrid_rgb]: demo/assets/image/dz_hybrid_rgb.png "No deadzone"
