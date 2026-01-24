import { describe, it, expect } from "vitest";
import * as sorting from "../../src/2026/sorting.js";

describe("bubbleSort", () => {
  it.fails("sorts simple array", () => {
    const arr = [3, 1, 4, 1, 5];
    sorting.bubbleSort(arr);
    expect(arr).toEqual([1, 1, 3, 4, 5]);
  });

  it.fails("handles already sorted", () => {
    const arr = [1, 2, 3, 4, 5];
    sorting.bubbleSort(arr);
    expect(arr).toEqual([1, 2, 3, 4, 5]);
  });

  it.fails("handles reverse sorted", () => {
    const arr = [5, 4, 3, 2, 1];
    sorting.bubbleSort(arr);
    expect(arr).toEqual([1, 2, 3, 4, 5]);
  });

  it.fails("handles single element", () => {
    const arr = [42];
    sorting.bubbleSort(arr);
    expect(arr).toEqual([42]);
  });
});

describe("selectionSort", () => {
  it.fails("sorts simple array", () => {
    const arr = [3, 1, 4, 1, 5];
    sorting.selectionSort(arr);
    expect(arr).toEqual([1, 1, 3, 4, 5]);
  });

  it.fails("handles negatives", () => {
    const arr = [3, -1, 4, -1, 5];
    sorting.selectionSort(arr);
    expect(arr).toEqual([-1, -1, 3, 4, 5]);
  });
});

describe("insertionSort", () => {
  it.fails("sorts simple array", () => {
    const arr = [3, 1, 4, 1, 5];
    sorting.insertionSort(arr);
    expect(arr).toEqual([1, 1, 3, 4, 5]);
  });

  it.fails("handles nearly sorted", () => {
    const arr = [1, 2, 4, 3, 5];
    sorting.insertionSort(arr);
    expect(arr).toEqual([1, 2, 3, 4, 5]);
  });
});

describe("mergeSort", () => {
  it.fails("sorts simple array", () => {
    expect(sorting.mergeSort([3, 1, 4, 1, 5])).toEqual([1, 1, 3, 4, 5]);
  });

  it.fails("handles empty", () => {
    expect(sorting.mergeSort([])).toEqual([]);
  });

  it.fails("handles single element", () => {
    expect(sorting.mergeSort([42])).toEqual([42]);
  });

  it.fails("handles large array", () => {
    const arr = Array.from({ length: 100 }, () => Math.floor(Math.random() * 1000));
    const sorted = sorting.mergeSort(arr);
    expect(sorted).toEqual([...arr].sort((a, b) => a - b));
  });
});

describe("quickSort", () => {
  it.fails("sorts simple array", () => {
    expect(sorting.quickSort([3, 1, 4, 1, 5])).toEqual([1, 1, 3, 4, 5]);
  });

  it.fails("handles empty", () => {
    expect(sorting.quickSort([])).toEqual([]);
  });

  it.fails("handles all duplicates", () => {
    expect(sorting.quickSort([5, 5, 5, 5])).toEqual([5, 5, 5, 5]);
  });
});

describe("countingSort", () => {
  it.fails("sorts simple array", () => {
    expect(sorting.countingSort([3, 1, 4, 1, 5])).toEqual([1, 1, 3, 4, 5]);
  });

  it.fails("handles zeros", () => {
    expect(sorting.countingSort([0, 0, 1, 0])).toEqual([0, 0, 0, 1]);
  });
});

describe("radixSort", () => {
  it.fails("sorts multi-digit numbers", () => {
    expect(sorting.radixSort([170, 45, 75, 90, 802, 24, 2, 66])).toEqual([
      2, 24, 45, 66, 75, 90, 170, 802,
    ]);
  });

  it.fails("sorts single-digit numbers", () => {
    expect(sorting.radixSort([3, 1, 4, 1, 5])).toEqual([1, 1, 3, 4, 5]);
  });
});
