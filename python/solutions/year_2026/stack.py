"""Stack data structure and stack-based problems."""


class Stack:
    """Basic stack with push, pop, peek, and is_empty operations."""

    def __init__(self):
        self._stack = []

    def push(self, value) -> None:
        """Add value to the top of the stack."""
        self._stack.append(value)

    def pop(self):
        """Remove and return the top value. Return None if empty."""
        if self.is_empty():
            return None
        return self._stack.pop()

    def peek(self):
        """Return the top value without removing it. Return None if empty."""
        return self._stack[-1]

    def is_empty(self):
        """Return True if stack has no elements."""
        return len(self._stack) == 0

    def __repr__(self):
        return "<Stack@{} = `{}`>".format(id(self), "".join(self._stack))


def valid_parentheses(s):
    """Return True if s has balanced brackets: (), [], {}. Handle nesting."""
    starts = "[{("
    ends = "]})"
    stack = Stack()
    for c in s:
        if c in starts:
            stack.push(c)
        elif c in ends:
            last = stack.pop()
            if last is None:
                return False
            if last in ends:
                stack.push(last)
                stack.push(c)
            elif starts.index(last) != ends.index(c):
                stack.push(last)
                stack.push(c)
    return stack.is_empty()


def evaluate_postfix(tokens):
    """Evaluate a postfix (reverse Polish) expression. Tokens are numbers or operators (+, -, *, /)."""
    raise NotImplementedError


class MinStack:
    """Stack that supports push, pop, peek, and get_min all in O(1) time."""

    def __init__(self):
        raise NotImplementedError

    def push(self, value):
        """Add value to the stack."""
        raise NotImplementedError

    def pop(self):
        """Remove and return the top value."""
        raise NotImplementedError

    def peek(self):
        """Return the top value without removing it."""
        raise NotImplementedError

    def get_min(self):
        """Return the minimum value in the stack in O(1) time."""
        raise NotImplementedError
