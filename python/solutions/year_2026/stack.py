"""Stack data structure and stack-based problems."""


class Stack:
    """Basic stack with push, pop, peek, and is_empty operations."""

    def __init__(self):
        raise NotImplementedError

    def push(self, value):
        """Add value to the top of the stack."""
        raise NotImplementedError

    def pop(self):
        """Remove and return the top value. Return None if empty."""
        raise NotImplementedError

    def peek(self):
        """Return the top value without removing it. Return None if empty."""
        raise NotImplementedError

    def is_empty(self):
        """Return True if stack has no elements."""
        raise NotImplementedError


def valid_parentheses(s):
    """Return True if s has balanced brackets: (), [], {}. Handle nesting."""
    raise NotImplementedError


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
