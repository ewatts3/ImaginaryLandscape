import pyglet

window= pyglet.window.Window()
player = pyglet.media.Player()
source = pyglet.media.load(r'Video\StockVideos\1.mp4')
player.queue(source)
player.play()

pyglet.app.run()