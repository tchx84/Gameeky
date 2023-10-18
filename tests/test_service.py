import pytest

from unittest.mock import Mock

from gi.repository import GLib

from valley.common.action import Action
from valley.common.direction import Direction
from valley.common.utils import get_data_path
from valley.common.scanner import Scanner
from valley.server.game.entity import EntityRegistry
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


def find_entity_by_id(entities, id):
    return next((e for e in entities if e.id == id), None)


def wait_for_seconds(seconds):
    mock = Mock()

    GLib.timeout_add_seconds(seconds, mock)

    while not mock.called:
        update()


def update():
    while context.pending():
        context.iteration(True)


def setup_module():
    global context

    mainloop = GLib.MainLoop.new(None, True)
    context = mainloop.get_context()


@pytest.mark.timeout(5)
def test_scanner_register():
    mock = Mock()

    scanner = Scanner(get_data_path("entities"))
    scanner.connect("found", lambda _, d: EntityRegistry.register(d))
    scanner.connect("done", mock)
    scanner.scan()

    while not mock.called:
        update()


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
    # See data/scene/sample.json
    assert len(server.scene.entities) == 5

    entity = find_entity_by_id(server.scene.entities, 4)

    assert entity.position.x == 0


@pytest.mark.timeout(5)
def test_client_message():
    mock = Mock()

    server.connect("updated", mock)
    client.message(Action.MOVE, Direction.RIGHT)

    while not mock.called:
        update()


@pytest.mark.timeout(5)
def test_server_tick():
    wait_for_seconds(2)

    entity = find_entity_by_id(server.scene.entities, 4)

    assert entity.position.x == 1


@pytest.mark.timeout(5)
def test_client_request_scene_update():
    mock = Mock()

    client.connect("updated", mock)
    client.request()

    while not mock.called:
        update()

    scene = mock.call_args.args[-1]
    entity = find_entity_by_id(scene.entities, 4)

    assert entity.position.x == 1


@pytest.mark.timeout(5)
def test_server_action_idle():
    client.message(Action.IDLE, 0)
    wait_for_seconds(2)

    entity = find_entity_by_id(server.scene.entities, 4)

    assert entity.position.x == 1


@pytest.mark.timeout(10)
def test_server_action_take():
    entity_moving = find_entity_by_id(server.scene.entities, 4)
    entity_moved = find_entity_by_id(server.scene.entities, 3)

    assert entity_moved.position.x == 1

    client.message(Action.MOVE, Direction.DOWN)
    wait_for_seconds(3)

    client.message(Action.TAKE, 0)
    wait_for_seconds(3)

    client.message(Action.MOVE, Direction.LEFT)
    wait_for_seconds(3)

    assert entity_moving.position.x == 0
    assert entity_moved.position.x == -1


@pytest.mark.timeout(5)
def test_server_action_drop():
    entity_moving = find_entity_by_id(server.scene.entities, 4)
    entity_moved = find_entity_by_id(server.scene.entities, 3)

    client.message(Action.DROP, 0)
    wait_for_seconds(2)

    client.message(Action.MOVE, Direction.RIGHT)
    wait_for_seconds(2)

    assert entity_moving.position.x == 1
    assert entity_moved.position.x == -1


@pytest.mark.timeout(10)
def test_server_attribute_durability():
    entity = find_entity_by_id(server.scene.entities, 2)

    assert entity.durability == 100

    client.message(Action.MOVE, Direction.LEFT)
    wait_for_seconds(2)

    client.message(Action.MOVE, Direction.DOWN)
    wait_for_seconds(2)

    client.message(Action.USE, 0)
    wait_for_seconds(4)

    entity = find_entity_by_id(server.scene.entities, 2)

    assert entity is None


@pytest.mark.timeout(10)
def test_server_attribute_stamina():
    entity = find_entity_by_id(server.scene.entities, 4)

    # Wait to full restore
    client.message(Action.IDLE, 0)
    wait_for_seconds(6)

    # See data/entities/sample.json
    assert entity.stamina == 100

    client.message(Action.USE, 0)
    wait_for_seconds(1)

    assert entity.stamina < 100


@pytest.mark.timeout(5)
def test_client_unregister():
    mock = Mock()

    server.connect("unregistered", mock)
    client.unregister()

    while not mock.called:
        update()


def test_server_is_empty():
    # See data/scene/sample.json
    assert len(server.scene.entities) == 3


def test_server_shutdown():
    server.shutdown()
