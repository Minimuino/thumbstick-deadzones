var DeadzoneDemo =
{
	// Global variables
};

DeadzoneDemo.Boot = function(game) {};

DeadzoneDemo.Boot.prototype =
{
	preload: function()
	{
		this.load.image('phaser', 'assets/image/phaser-dude.png');
		this.load.image('background', 'assets/image/checkerboard.png');
	},

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
