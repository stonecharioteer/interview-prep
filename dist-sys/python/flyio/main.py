"""Main interface for the maelstrom adapter"""

from __future__ import annotations
import sys
import json
import uuid


class MaelstromNode:
    def __init__(self):
        self._nodes = []
        self._recieved_messages = None
        self._topology = None

    def init_connection(self, inp: dict) -> dict:
        self._nodes = inp["body"]["node_ids"]
        out = self.prep_response(inp)
        out["body"]["type"] = "init_ok"
        return out

    def broadcast(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        out["body"]["type"] = "broadcast_ok"
        msg = out["body"].pop("message")
        if self._recieved_messages is None:
            self._recieved_messages = [msg]
        else:
            self._recieved_messages.append(msg)

        return out

    def read(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        out["body"]["type"] = "read_ok"
        out["body"]["messages"] = self._recieved_messages
        return out

    def process(self, inp: dict) -> dict:
        _type = inp["body"]["type"]
        if _type == "echo":
            return self.handle_echo(inp)
        elif _type == "init":
            return self.init_connection(inp)
        elif _type == "generate":
            return self.generate(inp)
        elif _type == "broadcast":
            return self.broadcast(inp)
        elif _type == "read":
            return self.read(inp)
        elif _type == "topology":
            return self.topology(inp)
        else:
            raise NotImplementedError()

    def topology(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        self._topology = out["body"]["topology"]
        out["body"]["type"] = "topology_ok"
        _ = out["body"].pop("topology")
        return out

    def handle_echo(self, inp: dict) -> dict:
        """Transforms an input from the maelstrom server to the expected output"""
        out = self.prep_response(inp)
        out["body"]["type"] = "echo_ok"
        return out

    def prep_response(self, inp: dict) -> dict:
        out = inp
        msg_id = out["body"].pop("msg_id")
        out["src"], out["dest"] = out["dest"], out["src"]
        out["body"]["in_reply_to"] = msg_id
        return out

    def generate(self, inp: dict) -> dict:
        out = self.prep_response(inp)
        out["body"]["type"] = "generate_ok"
        out["body"]["id"] = str(uuid.uuid4())
        return out


if __name__ == "__main__":
    node = MaelstromNode()
    for line in sys.stdin:
        message = json.loads(line)
        resp = node.process(message)
        print(json.dumps(resp), flush=True)
