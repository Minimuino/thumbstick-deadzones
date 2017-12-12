DeadzoneDemo.Main = function(game)
{
	this.player;
	this.pad1;
	this.dz_value;
	this.dz_type;
	this.dz_names = ["None", "Axial", "Radial", "Scaled Axial", "Scaled Radial", "Hybrid"];
	this.display_text;
	this.display_img;

	this.dbg_string;
};

DeadzoneDemo.Main.prototype =
{
	create: function()
	{
		this.add.sprite(0, 0, 'background');
		this.player = this.add.sprite(300, 300, 'phaser');
		this.player.anchor.setTo(0.5, 0.5);

		// Text box
		var text_bar = this.add.graphics();
		text_bar.beginFill(0x000000, 0.6);
		text_bar.drawRect(0, 30, 400, 110);
		text_bar.beginFill(0xffffff, 0.7);
		text_bar.drawRect(25, 35, 98, 98);
		var text_style = { font: "bold 32px Arial", fill: "#fff", boundsAlignV: "top" };
		this.display_text = this.add.text(0, 0, this.dz_names[1], text_style);
		this.display_text.setShadow(3, 3, 'rgba(0,0,0,0.6)', 2);
		this.display_text.setTextBounds(150, 40, 400, 100);
		this.display_img = this.add.sprite(30, 40, 'img_dz_None');
		this.display_img.scale.setTo(0.22, 0.22);

		this.input.gamepad.start();
		this.input.gamepad.setDeadZones(0.0);
		this.dz_value = 0.17;
		this.dz_type = 1;

		// To listen to buttons from a specific pad listen directly on that pad game.input.gamepad.padX, where X = pad 1-4
		this.pad1 = this.input.gamepad.pad1;
		this.pad1.addCallbacks(this, { onConnect: this.addButtons });
	},

	addButtons: function()
	{
		this.pad1.onDownCallback = this.onButtonDown;
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
		var name = this.dz_names[this.dz_type];
		return dz_functions[name](stick_input, this.dz_value);
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
			this.dbg_string = "Delta: " + delta.x + ", " + delta.y + ", dz_type: " + this.dz_type;
			this.player.x += delta.x * 10;
			this.player.y += delta.y * 10;
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
