import pytest

from src.year_2026 import stack

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


class TestEvaluatePostfix:
    def test_simple_add(self):
        assert stack.evaluate_postfix(["2", "3", "+"]) == 5

    def test_simple_multiply(self):
        assert stack.evaluate_postfix(["2", "3", "*"]) == 6

    def test_complex(self):
        assert stack.evaluate_postfix(["2", "1", "+", "3", "*"]) == 9

    def test_division(self):
        assert stack.evaluate_postfix(["4", "2", "/"]) == 2

    def test_complicated_0(self):
        assert stack.evaluate_postfix(list("2 5 + 3 -".split())) == 4
         
    def test_complicated_1(self):
        assert stack.evaluate_postfix(list("5 1 2 + 4 * + 3 -".split())) == 14

    def test_complicated_2(self):
        assert stack.evaluate_postfix("10 6 2 / 3 * -".split()) == 1
        assert stack.evaluate_postfix("1 2 + 3 + 4 +".split()) == 10
        assert stack.evaluate_postfix("1 2 3 4 5 * + * +".split()) == 47
        assert stack.evaluate_postfix("7 2 / 3 +".split()) == 6.5

    def test_invalid_raises_value_error(self):
        with pytest.raises(ValueError):
            samples = [
                "3 + 4",
                "1 +",
                "1 2 3 +",
                "",
            ]
            for sample in samples:
                stack.evaluate_postfix(sample.split())


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
