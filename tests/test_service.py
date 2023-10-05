import pytest

from unittest.mock import Mock

from gi.repository import GLib

from valley.common.action import Action
from valley.server.game.service import Service as Server
from valley.client.game.service import Service as Client

CLIENTS = 1
SESSION_PORT = 9996
UPDATES_PORT = 9997
SCENE_PORT = 9999
ADDRESS = "127.0.0.1"

context = None
server = None
client = None


def update():
    while context.pending():
        context.iteration(True)


def setup_module():
    global context

    mainloop = GLib.MainLoop.new(None, True)
    context = mainloop.get_context()


def test_server_create():
    global server

    server = Server(
        clients=CLIENTS,
        session_port=SESSION_PORT,
        updates_port=UPDATES_PORT,
        scene_port=SCENE_PORT,
        context=context,
    )

    update()


def test_client_create():
    global client

    client = Client(
        address=ADDRESS,
        session_port=SESSION_PORT,
        updates_port=UPDATES_PORT,
        scene_port=SCENE_PORT,
        context=context,
    )

    update()


@pytest.mark.timeout(5)
def test_client_register():
    mock = Mock()

    client.connect("registered", mock)
    client.register()

    while not mock.called:
        update()


def test_server_is_populated():
    assert len(server.scene.entities) == 1


@pytest.mark.timeout(5)
def test_client_report():
    mock = Mock()

    server.scene.connect("ticked", mock)
    client.report(Action.MOVE)

    while not mock.called:
        update()


@pytest.mark.timeout(5)
def test_client_request():
    mock = Mock()

    client.connect("updated", mock)
    client.request()

    while not mock.called:
        update()

    # Confirm that it moved
    scene = mock.call_args.args[-1]
    assert scene.entities[-1].position.x == 1.0


@pytest.mark.timeout(5)
def test_client_unregister():
    mock = Mock()

    server.connect("unregistered", mock)
    client.unregister()

    while not mock.called:
        update()


def test_server_is_empty():
    assert len(server.scene.entities) == 0
