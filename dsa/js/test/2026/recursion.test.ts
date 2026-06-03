import { describe, it, expect } from "vitest";
import * as recursion from "../../src/2026/recursion.js";

describe("factorial", () => {
  it.fails("returns 1 for 0", () => {
    expect(recursion.factorial(0)).toBe(1);
  });

  it.fails("returns 1 for 1", () => {
    expect(recursion.factorial(1)).toBe(1);
  });

  it.fails("calculates factorial of 5", () => {
    expect(recursion.factorial(5)).toBe(120);
  });

  it.fails("calculates factorial of 10", () => {
    expect(recursion.factorial(10)).toBe(3_628_800);
  });
});

describe("factorialMemo", () => {
  it.fails("returns 1 for 0", () => {
    expect(recursion.factorialMemo(0)).toBe(1);
  });

  it.fails("returns 1 for 1", () => {
    expect(recursion.factorialMemo(1)).toBe(1);
  });

  it.fails("calculates factorial of 5", () => {
    expect(recursion.factorialMemo(5)).toBe(120);
  });

  it.fails("calculates factorial of 10", () => {
    expect(recursion.factorialMemo(10)).toBe(3_628_800);
  });
});

describe("sumArray", () => {
  it.fails("sums simple array", () => {
    expect(recursion.sumArray([1, 2, 3, 4, 5])).toBe(15);
  });

  it.fails("sums single element", () => {
    expect(recursion.sumArray([42])).toBe(42);
  });

  it.fails("returns 0 for empty", () => {
    expect(recursion.sumArray([])).toBe(0);
  });

  it.fails("handles negatives", () => {
    expect(recursion.sumArray([-1, -2, 3])).toBe(0);
  });
});

describe("reverseString", () => {
  it.fails("reverses simple string", () => {
    expect(recursion.reverseString("hello")).toBe("olleh");
  });

  it.fails("reverses single char", () => {
    expect(recursion.reverseString("a")).toBe("a");
  });

  it.fails("returns empty for empty", () => {
    expect(recursion.reverseString("")).toBe("");
  });

  it.fails("handles palindrome", () => {
    expect(recursion.reverseString("radar")).toBe("radar");
  });
});

describe("power", () => {
  it.fails("returns 1 for exponent 0", () => {
    expect(recursion.power(2, 0)).toBe(1);
  });

  it.fails("calculates simple power", () => {
    expect(recursion.power(2, 3)).toBe(8);
  });

  it.fails("returns base for exponent 1", () => {
    expect(recursion.power(5, 1)).toBe(5);
  });

  it.fails("calculates larger power", () => {
    expect(recursion.power(2, 10)).toBe(1024);
  });
});

describe("powerMemo", () => {
  it.fails("returns 1 for exponent 0", () => {
    expect(recursion.powerMemo(2, 0)).toBe(1);
  });

  it.fails("calculates simple power", () => {
    expect(recursion.powerMemo(2, 3)).toBe(8);
  });

  it.fails("returns base for exponent 1", () => {
    expect(recursion.powerMemo(5, 1)).toBe(5);
  });

  it.fails("calculates larger power", () => {
    expect(recursion.powerMemo(2, 10)).toBe(1024);
  });
});

describe("fibonacci", () => {
  it.fails("returns base cases", () => {
    expect(recursion.fibonacci(0)).toBe(0);
    expect(recursion.fibonacci(1)).toBe(1);
  });

  it.fails("calculates fib(10)", () => {
    expect(recursion.fibonacci(10)).toBe(55);
  });

  it.fails("calculates fib(20)", () => {
    expect(recursion.fibonacci(20)).toBe(6765);
  });
});

describe("fibonacciMemo", () => {
  it.fails("returns base cases", () => {
    expect(recursion.fibonacciMemo(0)).toBe(0);
    expect(recursion.fibonacciMemo(1)).toBe(1);
  });

  it.fails("calculates fib(10)", () => {
    expect(recursion.fibonacciMemo(10)).toBe(55);
  });

  it.fails("calculates fib(30) efficiently", () => {
    expect(recursion.fibonacciMemo(30)).toBe(832_040);
  });
});
