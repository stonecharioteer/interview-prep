from interview_prep import lib


def test_binary_search():
    """Tests that the binary search algorithm works."""
    from random import randint

    for i in range(randint(5, 10**3)):
        sample_array = sorted(
            list(set([randint(1, 1000) for _ in range(randint(5, 10**2))]))
        )
        length = len(sample_array)
        target_position = randint(0, len(sample_array) - 1)
        target = sample_array[target_position]
        print(sample_array, target, target_position)
        result = lib.binary_search(sample_array, target)
        assert (
            result == target_position
        ), f"Binary search failed. Loop: {i+1}, array length={length}"
