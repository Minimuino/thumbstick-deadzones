/*
	Copyright (C) 2017 Carlos Pérez Ramil

	This file is part of Thumbstick Deadzones project.

	The Thumbstick Deadzones project is free software: you can redistribute it
	and/or modify it under the terms of the GNU General Public License as
	published by the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	The Thumbstick Deadzones project is distributed in the hope that it will be
	useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with the Thumbstick Deadzones project.
	If not, see <http://www.gnu.org/licenses/>.
*/

var DeadzoneDemo =
{
	// Global variables
};

DeadzoneDemo.Boot = function(game) {};

DeadzoneDemo.Boot.prototype =
{
	create: function()
	{
		this.input.maxPointers = 1;
		// this.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
		this.scale.pageAlignHorizontally = true;
		this.scale.pageAlignVertically = true;
		// this.scale.setScreenSize(true);
		this.state.start('Preloader');
	}
};
