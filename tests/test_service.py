import pytest

from unittest.mock import Mock

from gi.repository import GLib

from valley.common.action import Action
from valley.server.game.service import Service as Server
from valley.client.game.service import Service as Client
from valley.common.definitions import (
    DEFAULT_ADDRESS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
    DEFAULT_SCENE_PORT,
)

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
        clients=1,
        session_port=DEFAULT_SESSION_PORT,
        messages_port=DEFAULT_MESSAGES_PORT,
        scene_port=DEFAULT_SCENE_PORT,
        context=context,
    )

    update()


def test_client_create():
    global client

    client = Client(
        address=DEFAULT_ADDRESS,
        session_port=DEFAULT_SESSION_PORT,
        messages_port=DEFAULT_MESSAGES_PORT,
        scene_port=DEFAULT_SCENE_PORT,
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
    assert server.scene.entities[0].position.x == 0


@pytest.mark.timeout(5)
def test_client_message():
    mock = Mock()

    server.connect("updated", mock)
    client.message(Action.MOVE, 0)

    while not mock.called:
        update()

    # Force the scene to process the message and don't depend on timing
    server.scene.tick()

    assert server.scene.entities[0].position.x > 0


@pytest.mark.timeout(5)
def test_client_request():
    mock = Mock()

    client.connect("updated", mock)
    client.request()

    while not mock.called:
        update()

    # Confirm that it moved
    scene = mock.call_args.args[-1]
    assert scene.entities[-1].position.x > 0


@pytest.mark.timeout(5)
def test_client_unregister():
    mock = Mock()

    server.connect("unregistered", mock)
    client.unregister()

    while not mock.called:
        update()


def test_server_is_empty():
    assert len(server.scene.entities) == 0


def test_server_shutdown():
    server.shutdown()
