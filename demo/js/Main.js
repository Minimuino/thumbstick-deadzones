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

DeadzoneDemo.Main = function(game)
{
	this.player;
	this.pad1;
	this.dz_value;
	this.dz_type;
	this.dz_names = ["None", "Axial", "Radial", "Scaled Radial", "Sloped Axial", "Sloped Sc. Axial", "Hybrid"];
	this.display_text;
	this.display_img;

	this.dbg_string;
};

DeadzoneDemo.Main.prototype =
{
	create: function()
	{
		// World
		this.add.tileSprite(0, 0, 1920, 1920, 'background');
		this.world.setBounds(0, 0, 1920, 1920);
		this.player = this.add.sprite(this.world.centerX, this.world.centerY, 'phaser');
		this.player.anchor.setTo(0.5, 0.5);

		// Camera
		this.camera.follow(this.player, Phaser.Camera.FOLLOW_LOCKON, 0.1, 0.1);
		//this.camera.deadzone = new Phaser.Rectangle(100, 100, 600, 400);

		// Text box
		var text_bar = this.add.graphics();
		text_bar.beginFill(0x000000, 0.6);
		text_bar.drawRect(0, 30, 400, 110);
		text_bar.beginFill(0xffffff, 0.7);
		text_bar.drawRect(25, 35, 98, 98);
		var text_style = { font: "bold 32px Arial", fill: "#fff", boundsAlignV: "top" };
		this.display_text = this.add.text(0, 0, this.dz_names[0], text_style);
		this.display_text.setShadow(3, 3, 'rgba(0,0,0,0.6)', 2);
		this.display_text.setTextBounds(150, 40, 400, 100);
		this.display_img = this.add.sprite(30, 40, 'img_dz_None');
		this.display_img.scale.setTo(0.22, 0.22);
		text_bar.fixedToCamera = true;
		this.display_text.fixedToCamera = true;
		this.display_img.fixedToCamera = true;

		// Input
		this.input.gamepad.start();
		this.input.gamepad.setDeadZones(0.0);
		this.dz_value = 0.2;
		this.dz_type = 0;

		// To listen to buttons from a specific pad listen directly on that pad game.input.gamepad.padX, where X = pad 1-4
		this.pad1 = this.input.gamepad.pad1;
		this.pad1.addCallbacks(this, { onConnect: this.addButtons });
	},

	addButtons: function()
	{
		this.pad1.onDownCallback = this.onButtonDown;
	},

	mapRange: function(v, old_min, old_max, new_min, new_max)
	{
		return (new_min + (new_max - new_min) * (v - old_min) / (old_max - old_min));
	},

	dzNone: function(stick_input, deadzone)
	{
		return stick_input;
	},

	dzAxial: function(stick_input, deadzone)
	{
		var result = new Phaser.Point(
			(Math.abs(stick_input.x) > deadzone) ? stick_input.x : 0,
			(Math.abs(stick_input.y) > deadzone) ? stick_input.y : 0);
		return result;
	},

	dzRadial: function(stick_input, deadzone)
	{
		var magnitude = stick_input.getMagnitude();
		if (magnitude < deadzone)
			return new Phaser.Point(0, 0);
		else
			return stick_input;
	},

	dzScaledRadial: function(stick_input, deadzone)
	{
		var magnitude = stick_input.getMagnitude();
		if (magnitude < deadzone)
		{
			return new Phaser.Point(0, 0);
		}
		else
		{
			var input_normalized = Phaser.Point.normalize(stick_input);
			var result = new Phaser.Point();
			result.x = input_normalized.x * ((magnitude - deadzone) / (1 - deadzone));
			result.y = input_normalized.y * ((magnitude - deadzone) / (1 - deadzone));
			return result;
		}
	},

	dzSlopedAxial: function(stick_input, deadzone)
	{
		var deadzone_x = deadzone * Math.abs(stick_input.y);
		var deadzone_y = deadzone * Math.abs(stick_input.x);
		var result = new Phaser.Point(
			(Math.abs(stick_input.x) > deadzone_x) ? stick_input.x : 0,
			(Math.abs(stick_input.y) > deadzone_y) ? stick_input.y : 0);
		return result;
	},

	dzSlopedScaledAxial: function(stick_input, deadzone)
	{
		var deadzone_x = deadzone * Math.abs(stick_input.y);
		var deadzone_y = deadzone * Math.abs(stick_input.x);
		var sign = new Phaser.Point(Math.sign(stick_input.x), Math.sign(stick_input.y));
		var result = new Phaser.Point(0, 0);
		if (Math.abs(stick_input.x) > deadzone_x)
		{
			result.x = sign.x * this.mapRange(Math.abs(stick_input.x), deadzone_x, 1, 0, 1);
		}
		if (Math.abs(stick_input.y) > deadzone_y)
		{
			result.y = sign.y * this.mapRange(Math.abs(stick_input.y), deadzone_y, 1, 0, 1);
		}
		return result;
	},

	dzHybrid: function(stick_input, deadzone)
	{
		var deadzone_x = deadzone * Math.abs(stick_input.y);
		var deadzone_y = deadzone * Math.abs(stick_input.x);
		var sign = new Phaser.Point(Math.sign(stick_input.x), Math.sign(stick_input.y));
		var result = new Phaser.Point(0, 0);

		// First, check that input does not fall within deadzone
		if (stick_input.getMagnitude() < deadzone)
		{
			return result;
		}

		// Then apply a scaled_radial transformation
		var partial_output = this.dzScaledRadial(stick_input, deadzone);

		// Then apply a sloped_scaled_axial transformation
		var result = this.dzSlopedScaledAxial(partial_output, deadzone);

		return result;
	},

	applyDeadzone: function(stick_input)
	{
		var dz_functions = {
			"None": this.dzNone,
			"Axial": this.dzAxial,
			"Radial": this.dzRadial,
			"Scaled Axial": this.dzScaledAxial,
			"Scaled Radial": this.dzScaledRadial,
			"Sloped Axial": this.dzSlopedAxial,
			"Sloped Sc. Axial": this.dzSlopedScaledAxial,
			"Hybrid": this.dzHybrid
		};
		var name = this.dz_names[this.dz_type];
		return dz_functions[name].call(this, stick_input, this.dz_value);
	},

	update: function()
	{
		// Pad "connected or not" indicator
		/*
		if (game.input.gamepad.supported && game.input.gamepad.active && pad1.connected)
		{
			indicator.animations.frame = 0;
		}
		else
		{
			indicator.animations.frame = 1;
		}
		*/

		if (this.pad1.connected)
		{
			var left_stick_x = this.pad1.axis(Phaser.Gamepad.XBOX360_STICK_LEFT_X);
			var left_stick_y = this.pad1.axis(Phaser.Gamepad.XBOX360_STICK_LEFT_Y);

			var delta = this.applyDeadzone(new Phaser.Point(left_stick_x, left_stick_y));
			this.dbg_string = "Delta: " + delta.x + ", " + delta.y;
			this.player.x += delta.x * 6;
			this.player.y += delta.y * 6;
		}
	},

	onButtonDown: function(button_code)
	{
		// Update dz_type
		if (button_code == Phaser.Gamepad.XBOX360_LEFT_BUMPER)
		{
			this.dz_type = Math.max(this.dz_type - 1, 0);
		}
		else if (button_code == Phaser.Gamepad.XBOX360_RIGHT_BUMPER)
		{
			this.dz_type = Math.min(this.dz_type + 1, this.dz_names.length - 1);
		}

		// Update text box
		this.display_text.setText(this.dz_names[this.dz_type]);
		var texture_name = 'img_dz_' + this.dz_names[this.dz_type];
		this.display_img.loadTexture(texture_name);
	},

	render: function()
	{
		this.game.debug.text(this.dbg_string, 2, 515);
		//this.game.debug.text(this.dz_names[this.dz_type], 2, 12, "black");
	}
};
