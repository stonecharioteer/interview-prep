from flyio.echo.main import handle_echo


def test_handle_echo():
    """Tests that the echo function works"""
    _input = {
        "src": "c1",
        "dest": "n1",
        "body": {"type": "echo", "msg_id": 1, "echo": "Please echo 35"},
    }
    _output = {
        "src": "n1",
        "dest": "c1",
        "body": {"type": "echo_ok", "in_reply_to": 1, "echo": "Please echo 35"},
    }
    assert handle_echo(_input) == _output
