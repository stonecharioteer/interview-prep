import pytest

from solutions.year_2026 import backtracking

pytestmark = pytest.mark.backtracking


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestGenerateSubsets:
    def test_simple(self):
        result = backtracking.generate_subsets([1, 2])
        assert len(result) == 4
        assert [] in result
        assert [1] in result
        assert [2] in result
        assert [1, 2] in result

    def test_empty(self):
        assert backtracking.generate_subsets([]) == [[]]

    def test_three_elements(self):
        result = backtracking.generate_subsets([1, 2, 3])
        assert len(result) == 8


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestGeneratePermutations:
    def test_simple(self):
        result = backtracking.generate_permutations([1, 2])
        assert sorted(result) == [[1, 2], [2, 1]]

    def test_three_elements(self):
        result = backtracking.generate_permutations([1, 2, 3])
        assert len(result) == 6


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestGenerateCombinations:
    def test_simple(self):
        result = backtracking.generate_combinations(4, 2)
        expected = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        assert sorted(result) == sorted(expected)

    def test_n_choose_1(self):
        result = backtracking.generate_combinations(3, 1)
        assert sorted(result) == [[1], [2], [3]]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestGenerateParentheses:
    def test_one_pair(self):
        assert backtracking.generate_parentheses(1) == ["()"]

    def test_two_pairs(self):
        result = backtracking.generate_parentheses(2)
        assert sorted(result) == ["(())", "()()"]

    def test_three_pairs(self):
        result = backtracking.generate_parentheses(3)
        assert len(result) == 5


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestNQueens:
    def test_four_queens(self):
        result = backtracking.n_queens(4)
        assert len(result) == 2

    def test_one_queen(self):
        result = backtracking.n_queens(1)
        assert result == [[0]]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSudokuSolver:
    def test_simple(self):
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        backtracking.sudoku_solver(board)
        # Check that no zeros remain
        assert all(cell != 0 for row in board for cell in row)


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestWordSearch:
    def test_found(self):
        board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
        assert backtracking.word_search(board, "ABCCED") is True

    def test_not_found(self):
        board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
        assert backtracking.word_search(board, "ABCB") is False


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestCombinationSum:
    def test_simple(self):
        result = backtracking.combination_sum([2, 3, 6, 7], 7)
        expected = [[2, 2, 3], [7]]
        assert sorted([sorted(r) for r in result]) == sorted([sorted(e) for e in expected])


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestCombinationSum2:
    def test_simple(self):
        result = backtracking.combination_sum_2([10, 1, 2, 7, 6, 1, 5], 8)
        expected = [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
        assert sorted([sorted(r) for r in result]) == sorted([sorted(e) for e in expected])
