import { describe, it, expect } from "vitest";
import * as bits from "../../src/2026/bits.js";

describe("isPowerOfTwo", () => {
  it.fails("returns true for powers of two", () => {
    expect(bits.isPowerOfTwo(1)).toBe(true);
    expect(bits.isPowerOfTwo(2)).toBe(true);
    expect(bits.isPowerOfTwo(4)).toBe(true);
    expect(bits.isPowerOfTwo(1024)).toBe(true);
  });

  it.fails("returns false for non-powers", () => {
    expect(bits.isPowerOfTwo(0)).toBe(false);
    expect(bits.isPowerOfTwo(3)).toBe(false);
    expect(bits.isPowerOfTwo(6)).toBe(false);
    expect(bits.isPowerOfTwo(-4)).toBe(false);
  });
});

describe("countSetBits", () => {
  it.fails("counts bits correctly", () => {
    expect(bits.countSetBits(7)).toBe(3); // 111
    expect(bits.countSetBits(8)).toBe(1); // 1000
    expect(bits.countSetBits(0)).toBe(0);
  });

  it.fails("counts larger number", () => {
    expect(bits.countSetBits(255)).toBe(8); // 11111111
  });
});

describe("singleNumber", () => {
  it.fails("finds single in simple case", () => {
    expect(bits.singleNumber([2, 2, 1])).toBe(1);
  });

  it.fails("finds single in larger array", () => {
    expect(bits.singleNumber([4, 1, 2, 1, 2])).toBe(4);
  });

  it.fails("handles single element", () => {
    expect(bits.singleNumber([1])).toBe(1);
  });
});

describe("getBit", () => {
  it.fails("gets bit at position", () => {
    expect(bits.getBit(5, 0)).toBe(1); // 101, rightmost
    expect(bits.getBit(5, 1)).toBe(0); // 101, second from right
    expect(bits.getBit(5, 2)).toBe(1); // 101, third from right
  });
});

describe("setBit", () => {
  it.fails("sets bit at position", () => {
    expect(bits.setBit(5, 1)).toBe(7); // 101 -> 111
  });
});

describe("clearBit", () => {
  it.fails("clears bit at position", () => {
    expect(bits.clearBit(7, 1)).toBe(5); // 111 -> 101
  });
});

describe("subsetsBitmask", () => {
  it.fails("generates all subsets", () => {
    const result = bits.subsetsBitmask([1, 2]);
    expect(result).toHaveLength(4);
    expect(result).toContainEqual([]);
    expect(result).toContainEqual([1]);
    expect(result).toContainEqual([2]);
    expect(result).toContainEqual([1, 2]);
  });

  it.fails("handles empty array", () => {
    expect(bits.subsetsBitmask([])).toEqual([[]]);
  });
});
