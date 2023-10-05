from valley.common.action import Action
from valley.common.entity import Entity, Vector
from valley.common.message import Message
from valley.common.scene import Scene, SceneRequest
from valley.common.session import Session, SessionRequest


def test_serialize_vector():
    original = Vector(x=45, y=45)
    serialized = Vector.deserialize(original.serialize())

    assert serialized.x == original.x
    assert serialized.y == original.y


def test_serialize_entity():
    original = Entity(id=1, position=None, angle=0, velocity=0, action=Action.MOVE)
    serialized = Entity.deserialize(original.serialize())

    assert serialized.id == original.id
    assert serialized.angle == original.angle
    assert serialized.velocity == original.velocity
    assert serialized.action == original.action


def test_serialize_message():
    original = Message(session_id=90, action=Action.MOVE, sequence=180)
    serialized = Message.deserialize(original.serialize())

    assert serialized.session_id == original.session_id
    assert serialized.action == original.action
    assert serialized.sequence == original.sequence


def test_serialize_scene():
    original = Scene(entities=None)
    serialized = Scene.deserialize(original.serialize())

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
    original = SessionRequest()
    SessionRequest.deserialize(original.serialize())
