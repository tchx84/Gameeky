from valley.common.definitions import Action, Direction, State
from valley.common.entity import Entity, Vector
from valley.common.message import Message
from valley.common.scene import Scene, SceneRequest
from valley.common.session import Session, SessionRequest


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
    original = Session(id=360)
    serialized = Session.deserialize(original.serialize())

    assert serialized.id == original.id


def test_serialize_session_request():
    original = SessionRequest(type_id=0)
    serialized = SessionRequest.deserialize(original.serialize())

    assert original.type_id == serialized.type_id
