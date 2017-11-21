DeadzoneDemo.Main = function(game)
{
	this.player;
	this.pad1;
	this.dz_value;
	this.dz_type;

	this.dbg_string;
};

DeadzoneDemo.Main.prototype =
{
	create: function()
	{
		this.add.sprite(0, 0, 'background');
	    this.player = this.add.sprite(300, 300, 'phaser');
	    this.player.anchor.setTo(0.5, 0.5);

	    this.input.gamepad.start();
	    this.input.gamepad.setDeadZones(0.0);
	    this.dz_value = 0.17;
	    this.dz_type = "Axial";

	    // To listen to buttons from a specific pad listen directly on that pad game.input.gamepad.padX, where X = pad 1-4
	    this.pad1 = this.input.gamepad.pad1;
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
		return stick_input;
	},

	dzScaledAxial: function(stick_input, deadzone)
	{
		return stick_input;
	},

	dzScaledRadial: function(stick_input, deadzone)
	{
		return stick_input;
	},

	dzHybrid: function(stick_input, deadzone)
	{
		return stick_input;
	},

	applyDeadzone: function(stick_input)
	{
		var dz_functions = {
			"None": this.dzNone,
			"Axial": this.dzAxial,
			"Radial": this.dzRadial,
			"Scaled Axial": this.dzScaledAxial,
			"Scaled Radial": this.dzScaledRadial,
			"Hybrid": this.dzHybrid
		};
		return dz_functions[this.dz_type](stick_input, this.dz_value);
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
			this.player.x += delta.x * 10;
			this.player.y += delta.y * 10;
		}
	},

	render: function()
	{
		this.game.debug.text(this.dbg_string, 2, 515);
		this.game.debug.text(this.dz_type, 2, 12, "black");
	}
};
