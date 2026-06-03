"""Main interface for the maelstrom adapter"""

from __future__ import annotations
import sys
import json
import uuid


class GenericMaelstromNode:
    def __init__(self):
        self._nodes = []

    def prep_response(self, inp: dict) -> dict:
        out = inp
        msg_id = inp["body"]["msg_id"]
        out = {
            "src": inp["dest"],
            "dest": inp["src"],
            "body": {
                "in_reply_to": msg_id,
            },
        }
        return out

    def init_connection(self, inp: dict) -> dict:
        self._nodes = inp["body"]["node_ids"]
        out = self.prep_response(inp)
        out["body"]["type"] = "init_ok"
        return out

    def get_type(self, inp: dict) -> dict:
        return inp["body"]["type"]

    def process(self, inp: dict) -> dict:
        _type = self.get_type(inp)
        if _type == "init":
            return self.init_connection(inp)
        else:
            raise NotImplementedError(f"{_type} is not implemented.")


class EchoNode(GenericMaelstromNode):
    def __init__(self):
        super().__init__()

    def process(self, inp: dict) -> dict:
        _type = self.get_type(inp)
        if _type == "echo":
            return self.handle_echo(inp)
        return super().process(inp)

    def handle_echo(self, inp: dict) -> dict:
        """Transforms an input from the maelstrom server to the expected output"""
        out = self.prep_response(inp)
        out["body"]["type"] = "echo_ok"
        out["body"]["echo"] = inp["body"]["echo"]
        return out


class BroadcastNode(GenericMaelstromNode):
    def __init__(self):
        self._received_messages = []
        self._topology = None
        super().__init__()

    def process(self, inp: dict) -> dict:
        _type = self.get_type(inp)
        if _type == "broadcast":
            return self.broadcast(inp)
        elif _type == "read":
            return self.read(inp)
        elif _type == "topology":
            return self.topology(inp)
        return super().process(inp)

    def broadcast(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        out["body"]["type"] = "broadcast_ok"
        msg = inp["body"]["message"]
        self._received_messages.append(msg)
        return out

    def read(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        out["body"]["type"] = "read_ok"
        out["body"]["messages"] = self._received_messages
        return out

    def topology(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        self._topology = inp["body"]["topology"]
        out["body"]["type"] = "topology_ok"
        return out


class GeneratorNode(GenericMaelstromNode):
    def __init__(self):
        super().__init__()

    def process(self, inp: dict) -> dict:
        _type = self.get_type(inp)
        if _type == "generate":
            return self.generate(inp)
        return super().process(inp)

    def generate(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        out["body"]["type"] = "generate_ok"
        out["body"]["id"] = str(uuid.uuid4())
        return out


class AdderNode(GenericMaelstromNode):
    def __init__(self):
        self._count = 0
        super().__init__()

    def process(self, inp: dict) -> dict:
        _type = self.get_type(inp)
        if _type == "add":
            return self.add(inp)
        elif _type == "read":
            return self.read(inp)
        return super().process(inp)

    def add(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        out["body"]["type"] = "add_ok"
        self._count += inp["body"]["delta"]
        return out

    def read(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        out["body"]["type"] = "read_ok"
        out["body"]["value"] = self._count
        return out


if __name__ == "__main__":
    mode = sys.argv[1]
    node: GenericMaelstromNode
    if mode == "echo":
        node = EchoNode()
    elif mode == "generate":
        node = GeneratorNode()
    elif mode == "add":
        node = AdderNode()
    elif mode == "broadcast":
        node = BroadcastNode()
    else:
        sys.exit(1)
    for line in sys.stdin:
        message = json.loads(line)
        resp = node.process(message)
        print(json.dumps(resp), flush=True)
