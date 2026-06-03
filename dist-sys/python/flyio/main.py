"""Main interface for the maelstrom adapter"""

from __future__ import annotations
import sys
import json
import uuid


class MaelstromNode:
    def __init__(self):
        self._nodes = []

    def init_connection(self, inp: dict) -> dict:
        self._nodes = inp["body"]["node_ids"]
        out = self.prep_response(inp)
        out["body"]["type"] = "init_ok"
        return out

    def process(self, inp: dict) -> dict:
        if inp["body"]["type"] == "echo":
            return self.handle_echo(inp)
        elif inp["body"]["type"] == "init":
            return self.init_connection(inp)
        elif inp["body"]["type"] == "generate":
            return self.generate(inp)
        else:
            raise NotImplementedError()

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
