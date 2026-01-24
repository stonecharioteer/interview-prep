import { describe, it, expect } from "vitest";
import * as arrays from "../../src/2026/arrays.js";

describe("getRandomArray", () => {
  it.fails("returns array of correct size", () => {
    for (const size of [1, 5, 10, 50, 100]) {
      const result = arrays.getRandomArray(size);
      expect(result).toHaveLength(size);
    }
  });

  it.fails("generates values within expected range", () => {
    const result = arrays.getRandomArray(100);
    expect(result.every((x) => x >= 0 && x <= 100)).toBe(true);
  });
});

describe("getMax", () => {
  it.fails("finds max in random array", () => {
    const arr = [34, 12, 89, 45, 23];
    expect(arrays.getMax(arr)).toBe(89);
  });

  it.fails("finds max with single element", () => {
    expect(arrays.getMax([42])).toBe(42);
  });

  it.fails("finds max with negative numbers", () => {
    expect(arrays.getMax([-5, -10, -2, -100])).toBe(-2);
  });

  it.fails("finds max with duplicates", () => {
    expect(arrays.getMax([5, 10, 10, 3, 10])).toBe(10);
  });

  it.fails("finds max at different positions", () => {
    expect(arrays.getMax([100, 1, 2, 3])).toBe(100); // start
    expect(arrays.getMax([1, 2, 3, 100])).toBe(100); // end
    expect(arrays.getMax([1, 100, 2, 3])).toBe(100); // middle
  });
});

describe("getMin", () => {
  it.fails("finds min in random array", () => {
    const arr = [34, 12, 89, 45, 23];
    expect(arrays.getMin(arr)).toBe(12);
  });

  it.fails("finds min with single element", () => {
    expect(arrays.getMin([42])).toBe(42);
  });

  it.fails("finds min with negative numbers", () => {
    expect(arrays.getMin([-5, -10, -2, -100])).toBe(-100);
  });

  it.fails("finds min at different positions", () => {
    expect(arrays.getMin([1, 10, 20, 30])).toBe(1); // start
    expect(arrays.getMin([10, 20, 30, 1])).toBe(1); // end
    expect(arrays.getMin([10, 1, 20, 30])).toBe(1); // middle
  });
});

describe("getSum", () => {
  it.fails("sums array correctly", () => {
    expect(arrays.getSum([1, 2, 3, 4, 5])).toBe(15);
  });

  it.fails("sums single element", () => {
    expect(arrays.getSum([42])).toBe(42);
  });

  it.fails("sums with negative numbers", () => {
    expect(arrays.getSum([-5, 10, -2, 3])).toBe(6);
  });

  it.fails("sums to zero", () => {
    expect(arrays.getSum([5, -5, 10, -10])).toBe(0);
  });
});

describe("contains", () => {
  const sample = [1, 5, 10, 20, 50, 100];

  it.fails("finds existing element", () => {
    for (const n of sample) {
      expect(arrays.contains(sample, n)).toBe(true);
    }
  });

  it.fails("returns false for missing element", () => {
    expect(arrays.contains(sample, 999)).toBe(false);
    expect(arrays.contains(sample, -1)).toBe(false);
  });
});

describe("getAverage", () => {
  it.fails("calculates average correctly", () => {
    expect(arrays.getAverage([2, 4, 6, 8, 10])).toBe(6);
  });

  it.fails("handles single element", () => {
    expect(arrays.getAverage([42])).toBe(42);
  });

  it.fails("handles non-integer average", () => {
    expect(arrays.getAverage([1, 2, 3, 4])).toBe(2.5);
  });
});

describe("countOf", () => {
  it.fails("counts existing element", () => {
    expect(arrays.countOf([1, 2, 3, 2, 4, 2, 5], 2)).toBe(3);
  });

  it.fails("returns zero for missing element", () => {
    expect(arrays.countOf([1, 2, 3, 4, 5], 99)).toBe(0);
  });

  it.fails("counts all same elements", () => {
    expect(arrays.countOf([7, 7, 7, 7, 7], 7)).toBe(5);
  });
});

describe("findIndex", () => {
  it.fails("finds first occurrence", () => {
    expect(arrays.findIndex([10, 20, 30, 20, 40], 20)).toBe(1);
  });

  it.fails("returns null for missing", () => {
    expect(arrays.findIndex([1, 2, 3, 4, 5], 99)).toBeNull();
  });

  it.fails("finds at start", () => {
    expect(arrays.findIndex([10, 20, 30], 10)).toBe(0);
  });

  it.fails("finds at end", () => {
    expect(arrays.findIndex([10, 20, 30], 30)).toBe(2);
  });
});

describe("findAllIndices", () => {
  it.fails("finds all occurrences", () => {
    expect(arrays.findAllIndices([1, 2, 3, 2, 4, 2, 5], 2)).toEqual([1, 3, 5]);
  });

  it.fails("returns empty for missing", () => {
    expect(arrays.findAllIndices([1, 2, 3, 4, 5], 99)).toEqual([]);
  });

  it.fails("finds single occurrence", () => {
    expect(arrays.findAllIndices([1, 2, 3, 4, 5], 3)).toEqual([2]);
  });
});

describe("reversed", () => {
  it.fails("reverses simple array", () => {
    expect(arrays.reversed([1, 2, 3, 4, 5])).toEqual([5, 4, 3, 2, 1]);
  });

  it.fails("reverses single element", () => {
    expect(arrays.reversed([42])).toEqual([42]);
  });

  it.fails("does not modify original", () => {
    const original = [1, 2, 3, 4, 5];
    const copy = [...original];
    arrays.reversed(original);
    expect(original).toEqual(copy);
  });
});

describe("reverseInPlace", () => {
  it.fails("reverses simple array", () => {
    const arr = [1, 2, 3, 4, 5];
    arrays.reverseInPlace(arr);
    expect(arr).toEqual([5, 4, 3, 2, 1]);
  });

  it.fails("reverses even length", () => {
    const arr = [1, 2, 3, 4];
    arrays.reverseInPlace(arr);
    expect(arr).toEqual([4, 3, 2, 1]);
  });

  it.fails("reverses single element", () => {
    const arr = [42];
    arrays.reverseInPlace(arr);
    expect(arr).toEqual([42]);
  });
});

describe("isSorted", () => {
  it.fails("returns true for sorted ascending", () => {
    expect(arrays.isSorted([1, 2, 3, 4, 5])).toBe(true);
  });

  it.fails("returns true for sorted with duplicates", () => {
    expect(arrays.isSorted([1, 2, 2, 3, 4])).toBe(true);
  });

  it.fails("returns false for unsorted", () => {
    expect(arrays.isSorted([1, 3, 2, 4, 5])).toBe(false);
  });

  it.fails("returns true for single element", () => {
    expect(arrays.isSorted([42])).toBe(true);
  });

  it.fails("returns false for descending", () => {
    expect(arrays.isSorted([5, 4, 3, 2, 1])).toBe(false);
  });

  it.fails("returns true for all same elements", () => {
    expect(arrays.isSorted([7, 7, 7, 7])).toBe(true);
  });
});

describe("binarySearch", () => {
  it.fails("finds element in middle", () => {
    expect(arrays.binarySearch([1, 2, 3, 4, 5], 3)).toBe(2);
  });

  it.fails("finds element at start", () => {
    expect(arrays.binarySearch([1, 2, 3, 4, 5], 1)).toBe(0);
  });

  it.fails("finds element at end", () => {
    expect(arrays.binarySearch([1, 2, 3, 4, 5], 5)).toBe(4);
  });

  it.fails("returns null for missing", () => {
    expect(arrays.binarySearch([1, 2, 3, 4, 5], 99)).toBeNull();
  });

  it.fails("finds in larger array", () => {
    const arr = Array.from({ length: 500 }, (_, i) => i * 2);
    expect(arrays.binarySearch(arr, 500)).toBe(250);
  });
});

describe("mergeSorted", () => {
  it.fails("merges two sorted arrays", () => {
    expect(arrays.mergeSorted([1, 3, 5], [2, 4, 6])).toEqual([1, 2, 3, 4, 5, 6]);
  });

  it.fails("handles empty first array", () => {
    expect(arrays.mergeSorted([], [1, 2, 3])).toEqual([1, 2, 3]);
  });

  it.fails("handles empty second array", () => {
    expect(arrays.mergeSorted([1, 2, 3], [])).toEqual([1, 2, 3]);
  });

  it.fails("handles both empty", () => {
    expect(arrays.mergeSorted([], [])).toEqual([]);
  });

  it.fails("handles duplicates", () => {
    expect(arrays.mergeSorted([1, 2, 2], [2, 3, 3])).toEqual([1, 2, 2, 2, 3, 3]);
  });
});

describe("rotateK", () => {
  it.fails("rotates by one", () => {
    expect(arrays.rotateK([1, 2, 3, 4, 5], 1)).toEqual([5, 1, 2, 3, 4]);
  });

  it.fails("rotates by two", () => {
    expect(arrays.rotateK([1, 2, 3, 4, 5], 2)).toEqual([4, 5, 1, 2, 3]);
  });

  it.fails("rotates by zero", () => {
    expect(arrays.rotateK([1, 2, 3, 4, 5], 0)).toEqual([1, 2, 3, 4, 5]);
  });

  it.fails("rotates by length (no change)", () => {
    expect(arrays.rotateK([1, 2, 3, 4, 5], 5)).toEqual([1, 2, 3, 4, 5]);
  });

  it.fails("rotates by more than length", () => {
    expect(arrays.rotateK([1, 2, 3, 4, 5], 7)).toEqual([4, 5, 1, 2, 3]);
  });
});

describe("twoSum", () => {
  it.fails("finds pair", () => {
    const result = arrays.twoSum([2, 7, 11, 15], 9);
    expect(result).not.toBeNull();
    expect(result!.sort()).toEqual([0, 1]);
  });

  it.fails("returns null when no pair exists", () => {
    expect(arrays.twoSum([1, 2, 3], 100)).toBeNull();
  });

  it.fails("does not use same element twice", () => {
    const result = arrays.twoSum([3, 3], 6);
    expect(result).not.toBeNull();
    expect(new Set(result)).toHaveProperty("size", 2);
  });

  it.fails("handles negative numbers", () => {
    const result = arrays.twoSum([-1, -2, 3, 4], 2);
    expect(result).not.toBeNull();
  });
});

describe("removeDuplicatesSorted", () => {
  it.fails("removes duplicates", () => {
    expect(arrays.removeDuplicatesSorted([1, 1, 2, 2, 3])).toEqual([1, 2, 3]);
  });

  it.fails("handles no duplicates", () => {
    expect(arrays.removeDuplicatesSorted([1, 2, 3, 4, 5])).toEqual([1, 2, 3, 4, 5]);
  });

  it.fails("handles all duplicates", () => {
    expect(arrays.removeDuplicatesSorted([7, 7, 7, 7])).toEqual([7]);
  });

  it.fails("handles empty", () => {
    expect(arrays.removeDuplicatesSorted([])).toEqual([]);
  });
});

describe("partitionByPivot", () => {
  it.fails("partitions correctly", () => {
    const result = arrays.partitionByPivot([3, 1, 4, 1, 5, 9, 2, 6], 5);
    const pivotIdx = result.findIndex((v) => v >= 5);
    if (pivotIdx !== -1) {
      expect(result.slice(0, pivotIdx).every((v) => v < 5)).toBe(true);
      expect(result.slice(pivotIdx).every((v) => v >= 5)).toBe(true);
    }
  });

  it.fails("preserves elements", () => {
    const original = [3, 1, 4, 1, 5, 9, 2, 6];
    const result = arrays.partitionByPivot([...original], 5);
    expect(result.sort((a, b) => a - b)).toEqual(original.sort((a, b) => a - b));
  });
});

describe("slidingWindowSum", () => {
  it.fails("calculates window size 3", () => {
    expect(arrays.slidingWindowSum([1, 2, 3, 4, 5], 3)).toEqual([6, 9, 12]);
  });

  it.fails("calculates window size 1", () => {
    expect(arrays.slidingWindowSum([1, 2, 3, 4, 5], 1)).toEqual([1, 2, 3, 4, 5]);
  });

  it.fails("calculates window size equals length", () => {
    expect(arrays.slidingWindowSum([1, 2, 3, 4, 5], 5)).toEqual([15]);
  });

  it.fails("handles negative numbers", () => {
    expect(arrays.slidingWindowSum([1, -1, 2, -2, 3], 2)).toEqual([0, 1, 0, 1]);
  });
});

describe("maxSubarraySum", () => {
  it.fails("finds max in simple case", () => {
    expect(arrays.maxSubarraySum([1, 2, 3, 4, 5])).toBe(15);
  });

  it.fails("handles negative prefix", () => {
    expect(arrays.maxSubarraySum([-2, 1, -3, 4, -1, 2, 1, -5, 4])).toBe(6);
  });

  it.fails("handles all negative", () => {
    expect(arrays.maxSubarraySum([-1, -2, -3, -4])).toBe(-1);
  });

  it.fails("handles single element", () => {
    expect(arrays.maxSubarraySum([42])).toBe(42);
  });
});

describe("longestConsecutiveSequence", () => {
  it.fails("finds longest sequence", () => {
    expect(arrays.longestConsecutiveSequence([100, 4, 200, 1, 3, 2])).toBe(4);
  });

  it.fails("handles duplicates", () => {
    expect(arrays.longestConsecutiveSequence([1, 2, 0, 1])).toBe(3);
  });

  it.fails("handles empty", () => {
    expect(arrays.longestConsecutiveSequence([])).toBe(0);
  });

  it.fails("handles single element", () => {
    expect(arrays.longestConsecutiveSequence([5])).toBe(1);
  });
});
