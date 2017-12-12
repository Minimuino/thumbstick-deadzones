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

		this.load.image('phaser', 'assets/image/phaser-dude.png');
		this.load.image('background', 'assets/image/checkerboard.png');
		this.load.image('img_dz_None', 'assets/image/dz_none.png');
		this.load.image('img_dz_Axial', 'assets/image/dz_axial.png');
		this.load.image('img_dz_Radial', 'assets/image/dz_radial.png');
		this.load.image('img_dz_Scaled Axial', 'assets/image/dz_none.png');
		this.load.image('img_dz_Scaled Radial', 'assets/image/dz_scaled_radial.png');
		this.load.image('img_dz_Hybrid', 'assets/image/dz_none.png');
	},

	create: function()
	{
		this.state.start('Main');
	}
};
