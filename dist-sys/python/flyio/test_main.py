from copy import deepcopy

import pytest

from flyio.main import AdderNode, BroadcastNode, EchoNode, GeneratorNode


@pytest.fixture
def echo_node() -> EchoNode:
    return EchoNode()


@pytest.fixture
def broadcast_node() -> BroadcastNode:
    return BroadcastNode()


@pytest.fixture
def generator_node() -> GeneratorNode:
    return GeneratorNode()


@pytest.fixture
def adder_node() -> AdderNode:
    return AdderNode()


def test_echo_init_connection_returns_init_ok_and_stores_nodes(
    echo_node: EchoNode,
) -> None:
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

    response = echo_node.init_connection(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c0",
        "body": {
            "type": "init_ok",
            "in_reply_to": 1,
        },
    }
    assert echo_node._nodes == ["n1", "n2"]


def test_echo_returns_echo_ok_with_same_payload(echo_node: EchoNode) -> None:
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {
            "type": "echo",
            "msg_id": 2,
            "echo": "hello",
        },
    }

    response = echo_node.handle_echo(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "echo_ok",
            "in_reply_to": 2,
            "echo": "hello",
        },
    }


def test_echo_process_routes_supported_message_types(echo_node: EchoNode) -> None:
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

    assert echo_node.process(deepcopy(init))["body"]["type"] == "init_ok"
    assert echo_node.process(deepcopy(echo))["body"]["type"] == "echo_ok"


def test_echo_process_raises_for_unknown_message_type(echo_node: EchoNode) -> None:
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {"type": "unknown", "msg_id": 7},
    }

    with pytest.raises(NotImplementedError):
        echo_node.process(deepcopy(message))


def test_generate_returns_generate_ok_with_string_id(
    generator_node: GeneratorNode, monkeypatch: pytest.MonkeyPatch
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

    response = generator_node.generate(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "generate_ok",
            "in_reply_to": 3,
            "id": "generated-id",
        },
    }


def test_generator_process_routes_generate(generator_node: GeneratorNode) -> None:
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {"type": "generate", "msg_id": 3},
    }

    assert generator_node.process(deepcopy(message))["body"]["type"] == "generate_ok"


def test_topology_returns_topology_ok_and_stores_topology(
    broadcast_node: BroadcastNode,
) -> None:
    message = {
        "src": "c0",
        "dest": "n1",
        "body": {
            "type": "topology",
            "msg_id": 4,
            "topology": {"n1": ["n2"]},
        },
    }

    response = broadcast_node.topology(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c0",
        "body": {
            "type": "topology_ok",
            "in_reply_to": 4,
        },
    }
    assert broadcast_node._topology == {"n1": ["n2"]}


def test_broadcast_returns_broadcast_ok_and_records_message(
    broadcast_node: BroadcastNode,
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

    response = broadcast_node.broadcast(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "broadcast_ok",
            "in_reply_to": 5,
        },
    }
    assert broadcast_node._received_messages == [42]


def test_broadcast_read_returns_all_received_messages(
    broadcast_node: BroadcastNode,
) -> None:
    broadcast_node._received_messages = [1, 2, 3]
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {
            "type": "read",
            "msg_id": 6,
        },
    }

    response = broadcast_node.read(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "read_ok",
            "in_reply_to": 6,
            "messages": [1, 2, 3],
        },
    }


def test_broadcast_process_routes_supported_message_types(
    broadcast_node: BroadcastNode,
) -> None:
    init = {
        "src": "c0",
        "dest": "n1",
        "body": {"type": "init", "msg_id": 1, "node_id": "n1", "node_ids": ["n1"]},
    }
    topology = {
        "src": "c0",
        "dest": "n1",
        "body": {"type": "topology", "msg_id": 2, "topology": {"n1": []}},
    }
    broadcast = {
        "src": "c1",
        "dest": "n1",
        "body": {"type": "broadcast", "msg_id": 3, "message": 9},
    }
    read = {
        "src": "c1",
        "dest": "n1",
        "body": {"type": "read", "msg_id": 4},
    }

    assert broadcast_node.process(deepcopy(init))["body"]["type"] == "init_ok"
    assert broadcast_node.process(deepcopy(topology))["body"]["type"] == "topology_ok"
    assert broadcast_node.process(deepcopy(broadcast))["body"]["type"] == "broadcast_ok"
    assert broadcast_node.process(deepcopy(read))["body"]["type"] == "read_ok"


def test_add_initializes_counter(adder_node: AdderNode) -> None:
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {
            "type": "add",
            "msg_id": 7,
            "value": 5,
        },
    }

    response = adder_node.add(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "add_ok",
            "in_reply_to": 7,
        },
    }
    assert adder_node._count == 5


def test_add_increments_existing_counter(adder_node: AdderNode) -> None:
    adder_node._count = 5
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {
            "type": "add",
            "msg_id": 8,
            "value": 4,
        },
    }

    response = adder_node.add(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "add_ok",
            "in_reply_to": 8,
        },
    }
    assert adder_node._count == 9


def test_add_read_returns_counter_value(adder_node: AdderNode) -> None:
    adder_node._count = 9
    message = {
        "src": "c1",
        "dest": "n1",
        "body": {
            "type": "read",
            "msg_id": 9,
        },
    }

    response = adder_node.read(deepcopy(message))

    assert response == {
        "src": "n1",
        "dest": "c1",
        "body": {
            "type": "read_ok",
            "in_reply_to": 9,
            "value": 9,
        },
    }


def test_adder_process_routes_supported_message_types(adder_node: AdderNode) -> None:
    init = {
        "src": "c0",
        "dest": "n1",
        "body": {"type": "init", "msg_id": 1, "node_id": "n1", "node_ids": ["n1"]},
    }
    add = {
        "src": "c1",
        "dest": "n1",
        "body": {"type": "add", "msg_id": 2, "value": 3},
    }
    read = {
        "src": "c1",
        "dest": "n1",
        "body": {"type": "read", "msg_id": 3},
    }

    assert adder_node.process(deepcopy(init))["body"]["type"] == "init_ok"
    assert adder_node.process(deepcopy(add))["body"]["type"] == "add_ok"
    assert adder_node.process(deepcopy(read))["body"]["type"] == "read_ok"
