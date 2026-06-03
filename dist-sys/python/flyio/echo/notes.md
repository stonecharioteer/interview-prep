# Echo

In the echo challenge, we recieve an `echo` from `Maelstrom` that looks like

```json
{
  "src": "c1",
  "dest": "n1",
  "body": {
    "type": "echo",
    "msg_id": 1,
    "echo": "Please echo 35"
  }
}
```

Nodes and clients are sequentially numbered as `n1`, `n2` or `c1`, `c2` and we need to return
the same body to the client but with a message type of `echo_type`. It should associate itself with the original message by setting the `in_reply_to` field
to the original message ID.

It should look something like this:

```json
{
  "src": "n1",
  "dest": "c1",
  "body": {
    "type": "echo_ok",
    "in_reply_to": 1,
    "echo": "Please echo 35"
  }
}
```
