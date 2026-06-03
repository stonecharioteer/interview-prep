from copy import deepcopy

import pytest

from flyio.main import MaelstromNode


@pytest.fixture
def node() -> MaelstromNode:
    return MaelstromNode()


def test_init_connection_returns_init_ok_and_stores_nodes(node: MaelstromNode) -> None:
    message = {
        "src": "c0",
        "dest": "n1",
        "body": {
            "type": "init",
            "msg_id": 1,
            "node_id": "n1",
            "node_ids": ["n1", "n2"],
        },
    }

    response = node.init_connection(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c0",
        "body": {
            "type": "init_ok",
            "in_reply_to": 1,
        },
    }
    assert node._nodes == ["n1", "n2"]


def test_handle_echo_returns_echo_ok_with_same_payload(node: MaelstromNode) -> None:
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {
            "type": "echo",
            "msg_id": 2,
            "echo": "hello",
        },
    }

    response = node.handle_echo(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "echo_ok",
            "in_reply_to": 2,
            "echo": "hello",
        },
    }


def test_generate_returns_generate_ok_with_string_id(
    node: MaelstromNode, monkeypatch: pytest.MonkeyPatch
) -> None:
    class FakeUuid:
        def __str__(self) -> str:
            return "generated-id"

    monkeypatch.setattr("flyio.main.uuid.uuid4", lambda: FakeUuid())

    message = {
        "src": "c1",
        "dest": "n1",
        "body": {
            "type": "generate",
            "msg_id": 3,
        },
    }

    response = node.generate(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "generate_ok",
            "in_reply_to": 3,
            "id": "generated-id",
        },
    }


def test_topology_returns_topology_ok_and_stores_topology(node: MaelstromNode) -> None:
    message = {
        "src": "c0",
        "dest": "n1",
        "body": {
            "type": "topology",
            "msg_id": 4,
            "topology": {"n1": ["n2"]},
        },
    }

    response = node.topology(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c0",
        "body": {
            "type": "topology_ok",
            "in_reply_to": 4,
        },
    }
    assert node._topology == {"n1": ["n2"]}


def test_broadcast_returns_broadcast_ok_and_records_message(
    node: MaelstromNode,
) -> None:
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {
            "type": "broadcast",
            "msg_id": 5,
            "message": 42,
        },
    }

    response = node.broadcast(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "broadcast_ok",
            "in_reply_to": 5,
        },
    }
    assert node._received_messages == [42]


def test_read_returns_all_received_messages(node: MaelstromNode) -> None:
    node._received_messages = [1, 2, 3]
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {
            "type": "read",
            "msg_id": 6,
        },
    }

    response = node.read(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "read_ok",
            "in_reply_to": 6,
            "messages": [1, 2, 3],
        },
    }


def test_process_routes_supported_message_types(node: MaelstromNode) -> None:
    init = {
        "src": "c0",
        "dest": "n1",
        "body": {"type": "init", "msg_id": 1, "node_id": "n1", "node_ids": ["n1"]},
    }
    echo = {
        "src": "c1",
        "dest": "n1",
        "body": {"type": "echo", "msg_id": 2, "echo": "x"},
    }

    assert node.process(deepcopy(init))["body"]["type"] == "init_ok"
    assert node.process(deepcopy(echo))["body"]["type"] == "echo_ok"


def test_process_raises_for_unknown_message_type(node: MaelstromNode) -> None:
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {"type": "unknown", "msg_id": 7},
    }

    with pytest.raises(NotImplementedError):
        node.process(deepcopy(message))
