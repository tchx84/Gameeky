from gameeky.common.definitions import Action, Direction, State
from gameeky.common.vector import Vector
from gameeky.common.entity import Entity
from gameeky.common.message import Message
from gameeky.common.scene import Scene, SceneRequest
from gameeky.common.stats import Stats, StatsRequest
from gameeky.common.session import Session, SessionRequest
from gameeky.common.errors import Error


def test_serialize_vector():
    original = Vector(x=45, y=45, z=45)
    serialized = Vector.deserialize(original.serialize())

    assert serialized.x == original.x
    assert serialized.y == original.y
    assert serialized.z == original.z


def test_serialize_entity():
    original = Entity(
        id=1,
        type_id=1,
        position=None,
        direction=Direction.EAST,
        state=State.MOVING,
        visible=False,
        status=0.5,
        luminance=1.0,
    )
    serialized = Entity.deserialize(original.serialize())

    assert serialized.id == original.id
    assert serialized.direction == original.direction
    assert serialized.state == original.state
    assert serialized.visible == original.visible
    assert serialized.status == original.status
    assert serialized.luminance == original.luminance


def test_serialize_message():
    original = Message(session_id=90, action=Action.MOVE, value=360, sequence=180)
    serialized = Message.deserialize(original.serialize())

    assert serialized.session_id == original.session_id
    assert serialized.value == original.value
    assert serialized.action == original.action
    assert serialized.sequence == original.sequence


def test_serialize_scene():
    original = Scene(
        width=16,
        height=16,
        time=12,
        anchor=None,
        entities=None,
    )
    serialized = Scene.deserialize(original.serialize())

    assert original.time == serialized.time
    assert original.entities == serialized.entities


def test_serialize_scene_request():
    original = SceneRequest(session_id=90)
    serialized = SceneRequest.deserialize(original.serialize())

    assert serialized.session_id == original.session_id


def test_serialize_session():
    original = Session(id=360, error=Error.VERSION)
    serialized = Session.deserialize(original.serialize())

    assert serialized.id == original.id
    assert serialized.error == original.error


def test_serialize_session_request():
    original = SessionRequest(type_id=0, version="1.2.3", project="name")
    serialized = SessionRequest.deserialize(original.serialize())

    assert original.type_id == serialized.type_id
    assert original.version == serialized.version
    assert original.project == serialized.project


def test_serialize_stats():
    original = Stats(durability=1.0, stamina=1.0, held=2)
    serialized = Stats.deserialize(original.serialize())

    assert serialized.durability == original.durability
    assert serialized.stamina == original.stamina
    assert serialized.held == original.held


def test_serialize_stats_request():
    original = StatsRequest(session_id=1)
    serialized = StatsRequest.deserialize(original.serialize())

    assert original.session_id == serialized.session_id
