from valley.common.definitions import Direction

from valley.cli.game import Game


def on_updated(game: Game, elapsed: int) -> None:
    if elapsed < 1000:
        game.idle()
    elif elapsed < 2000:
        game.move(Direction.EAST)
    elif elapsed < 3000:
        game.move(Direction.WEST)
    elif elapsed < 4000:
        game.take()
    elif elapsed < 5000:
        game.use()
    elif elapsed < 6000:
        game.drop()
    elif elapsed < 7000:
        game.interact()
    elif elapsed < 8000:
        game.quit()


game = Game()
game.connect("updated", on_updated)
game.run()
