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
	},

	create: function()
	{
		this.state.start('Main');
	}
};
