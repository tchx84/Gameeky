from gi.repository import GLib

from valley.server.game.service import Service as Server


CLIENTS = 2
SESSION_PORT = 9998
UPDATES_PORT = 9997
SCENE_PORT = 9999

mainloop = GLib.MainLoop.new(None, True)
context = mainloop.get_context()

server = Server(
    clients=CLIENTS,
    session_port=SESSION_PORT,
    updates_port=UPDATES_PORT,
    scene_port=SCENE_PORT,
    context=context,
)

mainloop.run()
