Understanding thumbstick deadzones
==================================

What's this?
------------

Gamepads and similar thumbstick controllers usually give an input value between -1 and 1 in two axis. Thus, when the stick is idle the expected value is (0, 0). However, most of times the given value is near but not equal to 0. The idea of deadzone is like a threshold value for thumbstick input. Although it seems pretty simple, it can lead us into trouble if we don't implement it carefully.

This work is an extension of [this great article](http://www.third-helix.com/2013/04/12/doing-thumbstick-dead-zones-right.html) by Josh Sutphin. Here I'll go through different approaches for implementing deadzones, along with a playable demo. I hope this helps someone to choose the right one for her project.

Deadzone types
--------------

Under construction

First explain how to interpret the graphs.

Second discuss deadzone types.
