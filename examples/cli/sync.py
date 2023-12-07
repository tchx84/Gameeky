from gameeky.common.definitions import Direction

from gameeky.cli.game import Game


game = Game()
game.join()
game.idle(time=1000)
game.move(Direction.EAST, time=1000)
game.move(Direction.WEST, time=1000)
game.take(time=1000)
game.use(time=1000)
game.drop(time=1000)
game.interact(time=1000)
game.quit()
