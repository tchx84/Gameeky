import pytest

from unittest.mock import Mock

from gi.repository import GLib

from gameeky.common.utils import get_project_path
from gameeky.common.scanner import Scanner, Description
from gameeky.server.game.entity import EntityRegistry
from gameeky.server.game.service import Service as Server
from gameeky.client.game.service import Service as Client
from gameeky.common.definitions import (
    Action,
    Direction,
    EntityType,
    DEFAULT_SCENE,
    DEFAULT_ADDRESS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
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

    scanner = Scanner(get_project_path("entities"))
    scanner.connect(
        "found",
        lambda _, p: EntityRegistry.register(Description.new_from_json(p)),
    )
    scanner.connect("done", mock)
    scanner.scan()

    while not mock.called:
        update()


def test_server_create():
    global server

    server = Server(
        scene=DEFAULT_SCENE,
        clients=1,
        session_port=DEFAULT_SESSION_PORT,
        messages_port=DEFAULT_MESSAGES_PORT,
        context=context,
    )

    update()


def test_client_create():
    global client

    client = Client(
        entity_type=EntityType.PLAYER,
        address=DEFAULT_ADDRESS,
        session_port=DEFAULT_SESSION_PORT,
        messages_port=DEFAULT_MESSAGES_PORT,
        context=context,
        graceful=False,
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
    client.message(Action.MOVE, Direction.EAST)

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

    client.connect("scene-updated", mock)
    client.request_scene()

    while not mock.called:
        update()

    scene = mock.call_args.args[-1]
    entity = find_entity_by_id(scene.entities, 4)

    assert entity.position.x == 1


@pytest.mark.timeout(5)
def test_client_request_stats_update():
    mock = Mock()

    client.connect("stats-updated", mock)
    client.request_stats()

    while not mock.called:
        update()

    stats = mock.call_args.args[-1]

    assert stats.durability == 1
    assert stats.stamina == 1
    assert stats.held == EntityType.EMPTY


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

    client.message(Action.MOVE, Direction.SOUTH)
    wait_for_seconds(3)

    client.message(Action.TAKE, 0)
    wait_for_seconds(3)

    client.message(Action.MOVE, Direction.WEST)
    wait_for_seconds(3)

    assert entity_moving.position.x == 0
    assert entity_moved.position.x == 0


@pytest.mark.timeout(10)
def test_server_attribute_durability():
    entity = find_entity_by_id(server.scene.entities, 2)

    assert entity.durability == 100

    client.message(Action.MOVE, Direction.SOUTH)
    wait_for_seconds(2)

    client.message(Action.USE, 0)
    wait_for_seconds(4)

    entity = find_entity_by_id(server.scene.entities, 2)

    assert entity is None


@pytest.mark.timeout(15)
def test_server_attribute_stamina():
    entity = find_entity_by_id(server.scene.entities, 4)

    # Wait to full restore
    client.message(Action.IDLE, 0)
    wait_for_seconds(10)

    # See data/entities/sample.json
    assert entity.stamina == 100

    client.message(Action.USE, 0)
    wait_for_seconds(1)

    assert entity.stamina < 100


@pytest.mark.timeout(5)
def test_server_action_drop():
    entity_moving = find_entity_by_id(server.scene.entities, 4)
    entity_moved = find_entity_by_id(server.scene.entities, 3)

    assert entity_moving.position.x == 0

    client.message(Action.DROP, 0)
    wait_for_seconds(2)

    client.message(Action.MOVE, Direction.EAST)
    wait_for_seconds(2)

    assert entity_moving.position.x == 1
    assert entity_moved.position.x == 0


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
