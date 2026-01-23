import pytest

from solutions.year_2026 import stack

pytestmark = pytest.mark.stack


class TestStack:
    def test_push_pop(self):
        s = stack.Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_peek(self):
        s = stack.Stack()
        s.push(42)
        assert s.peek() == 42
        assert s.peek() == 42  # still there

    def test_is_empty(self):
        s = stack.Stack()
        assert s.is_empty() is True
        s.push(1)
        assert s.is_empty() is False

    def test_pop_empty(self):
        s = stack.Stack()
        assert s.pop() is None


class TestValidParentheses:
    def test_valid_simple(self):
        assert stack.valid_parentheses("()") is True
        assert stack.valid_parentheses("()[]{}") is True

    def test_valid_nested(self):
        assert stack.valid_parentheses("{[()]}") is True

    def test_invalid(self):
        assert stack.valid_parentheses("(]") is False
        assert stack.valid_parentheses("([)]") is False

    def test_empty(self):
        assert stack.valid_parentheses("") is True


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestEvaluatePostfix:
    def test_simple_add(self):
        assert stack.evaluate_postfix(["2", "3", "+"]) == 5

    def test_simple_multiply(self):
        assert stack.evaluate_postfix(["2", "3", "*"]) == 6

    def test_complex(self):
        assert stack.evaluate_postfix(["2", "1", "+", "3", "*"]) == 9

    def test_division(self):
        assert stack.evaluate_postfix(["4", "2", "/"]) == 2


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMinStack:
    def test_basic(self):
        s = stack.MinStack()
        s.push(3)
        s.push(1)
        s.push(2)
        assert s.get_min() == 1

    def test_after_pop(self):
        s = stack.MinStack()
        s.push(2)
        s.push(1)
        s.pop()
        assert s.get_min() == 2

    def test_duplicates(self):
        s = stack.MinStack()
        s.push(1)
        s.push(1)
        s.pop()
        assert s.get_min() == 1
