import { describe, it, expect } from "vitest";
import * as bs from "../../src/2026/binarySearch.js";

describe("findFirstOccurrence", () => {
  it.fails("finds first of multiple occurrences", () => {
    expect(bs.findFirstOccurrence([1, 2, 2, 2, 3], 2)).toBe(1);
  });

  it.fails("finds single occurrence", () => {
    expect(bs.findFirstOccurrence([1, 2, 3, 4, 5], 3)).toBe(2);
  });

  it.fails("returns -1 for not found", () => {
    expect(bs.findFirstOccurrence([1, 2, 3], 5)).toBe(-1);
  });

  it.fails("finds at start", () => {
    expect(bs.findFirstOccurrence([2, 2, 2, 3], 2)).toBe(0);
  });
});

describe("findLastOccurrence", () => {
  it.fails("finds last of multiple occurrences", () => {
    expect(bs.findLastOccurrence([1, 2, 2, 2, 3], 2)).toBe(3);
  });

  it.fails("finds at end", () => {
    expect(bs.findLastOccurrence([1, 2, 3, 3, 3], 3)).toBe(4);
  });
});

describe("searchInsertPosition", () => {
  it.fails("returns index if found", () => {
    expect(bs.searchInsertPosition([1, 3, 5, 6], 5)).toBe(2);
  });

  it.fails("returns insert position in middle", () => {
    expect(bs.searchInsertPosition([1, 3, 5, 6], 2)).toBe(1);
  });

  it.fails("returns insert position at end", () => {
    expect(bs.searchInsertPosition([1, 3, 5, 6], 7)).toBe(4);
  });

  it.fails("returns insert position at start", () => {
    expect(bs.searchInsertPosition([1, 3, 5, 6], 0)).toBe(0);
  });
});

describe("searchRotatedSortedArray", () => {
  it.fails("finds in left portion", () => {
    expect(bs.searchRotatedSortedArray([4, 5, 6, 7, 0, 1, 2], 0)).toBe(4);
  });

  it.fails("finds in right portion", () => {
    expect(bs.searchRotatedSortedArray([4, 5, 6, 7, 0, 1, 2], 5)).toBe(1);
  });

  it.fails("returns -1 for not found", () => {
    expect(bs.searchRotatedSortedArray([4, 5, 6, 7, 0, 1, 2], 3)).toBe(-1);
  });
});

describe("findMinRotatedSortedArray", () => {
  it.fails("finds min in rotated array", () => {
    expect(bs.findMinRotatedSortedArray([3, 4, 5, 1, 2])).toBe(1);
  });

  it.fails("finds min in non-rotated array", () => {
    expect(bs.findMinRotatedSortedArray([1, 2, 3, 4, 5])).toBe(1);
  });

  it.fails("handles single element", () => {
    expect(bs.findMinRotatedSortedArray([1])).toBe(1);
  });
});

describe("findPeakElement", () => {
  it.fails("finds peak in single-peak array", () => {
    expect(bs.findPeakElement([1, 2, 3, 1])).toBe(2);
  });

  it.fails("finds peak in ascending array", () => {
    expect(bs.findPeakElement([1, 2, 3, 4])).toBe(3);
  });

  it.fails("finds peak in descending array", () => {
    expect(bs.findPeakElement([4, 3, 2, 1])).toBe(0);
  });
});

describe("kokoEatingBananas", () => {
  it.fails("finds minimum eating speed", () => {
    expect(bs.kokoEatingBananas([3, 6, 7, 11], 8)).toBe(4);
  });

  it.fails("handles tight constraint", () => {
    expect(bs.kokoEatingBananas([30, 11, 23, 4, 20], 5)).toBe(30);
  });
});

describe("capacityToShipPackages", () => {
  it.fails("finds minimum capacity", () => {
    expect(bs.capacityToShipPackages([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)).toBe(15);
  });

  it.fails("handles single day", () => {
    expect(bs.capacityToShipPackages([1, 2, 3, 1, 1], 1)).toBe(8);
  });
});
