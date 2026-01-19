import random
from copy import deepcopy
from typing import List, Optional


def get_random_list(n: int = 50):
    return [random.randint(0, 100) for _ in range(n)]


def print_a_list(x: List[int]):
    for i in x:
        print(i)


def get_max_in_list(x: List[int]):
    m = None
    for i in x:
        if m is None or i > m:
            m = i
    return m


def get_sum_of_list(x: List[int]):
    s = 0
    for i in x:
        s += i
    return s


def is_n_in_list(x: List[int], n: int):
    print(f"{n=}")
    for i in x:
        if i == n:
            return True
    return False


def get_min_in_list(x: List[int]):
    m = None
    for i in x:
        if m is None or m > i:
            m = i
    return m


def get_average_of_list(x: List[int]) -> float:
    s = 0
    for i in x:
        s += i
    return s / len(x)


def count_instances(x: List[int], n: int) -> int:
    counter = 0
    for i in x:
        if i == n:
            counter += 1
    return counter


def find_index(x: List[int], n: int) -> Optional[int]:
    for ix, i in enumerate(x):
        if i == n:
            return ix


def find_all_indicies(x: List[int], n: int) -> List:
    indices = []
    for ix, i in enumerate(x):
        if i == n:
            indices.append(ix)
    return indices


def array_reversed(x: List[int]) -> List[int]:
    return x[::-1]


def array_reversed_in_place(x: List[int]):
    for ix in range(len(x) // 2):
        x[len(x) - 1 - ix], x[ix] = x[ix], x[len(x) - 1 - ix]


if __name__ == "__main__":
    x = get_random_list(10)
    print_a_list(x)
    assert max(x) == get_max_in_list(x)
    assert min(x) == get_min_in_list(x)
    assert sum(x) == get_sum_of_list(x)
    n = random.randint(0, 100)
    assert is_n_in_list(x, n) == (n in x), "Failed to detect if n is in x"
    assert count_instances(x, n) == x.count(n)
    if ix := find_index(x, n):
        assert ix == x.index(n)
    indices = find_all_indicies(x, n)  # TODO: Test this somehow?
    assert array_reversed(x) == list(reversed(x))
    y = deepcopy(x)
    array_reversed_in_place(y)
    assert y == list(reversed(x))
