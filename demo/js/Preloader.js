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

DeadzoneDemo.Preloader = function(game)
{

};

DeadzoneDemo.Preloader.prototype =
{
	preload: function()
	{
		// this.stage.backgroundColor = '#B4D9E7';
		// this.preloadBar = this.add.sprite((DeadzoneDemo.GAME_WIDTH-311)/2,
		//     (DeadzoneDemo.GAME_HEIGHT-27)/2, 'preloaderBar');
		// this.load.setPreloadSprite(this.preloadBar);

		// this.load.image('background', 'img/background.png');

		// this.load.spritesheet('candy', 'img/candy.png', 82, 98);

		// Debug plugin
		//this.add.plugin(Phaser.Plugin.Debug);

		this.load.image('phaser', 'assets/image/phaser-dude.png');
		this.load.image('background', 'assets/image/debug-grid-1920x1920.png');
		this.load.image('img_dz_None', 'assets/image/dz_none_gray.png');
		this.load.image('img_dz_Axial', 'assets/image/dz_axial_gray.png');
		this.load.image('img_dz_Radial', 'assets/image/dz_radial_gray.png');
		this.load.image('img_dz_Scaled Axial', 'assets/image/dz_none_gray.png');
		this.load.image('img_dz_Scaled Radial', 'assets/image/dz_scaled_radial_gray.png');
		this.load.image('img_dz_Sloped Axial', 'assets/image/dz_sloped_axial_rgb.png');
		this.load.image('img_dz_Sloped Sc. Axial', 'assets/image/dz_sloped_scaled_axial_rgb.png');
		this.load.image('img_dz_Hybrid', 'assets/image/dz_hybrid_rgb.png');
	},

	create: function()
	{
		this.state.start('Main');
	}
};
