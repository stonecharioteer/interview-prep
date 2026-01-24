import { describe, it, expect } from "vitest";
import { Stack, MinStack, validParentheses, evaluatePostfix } from "../../src/2026/stack.js";

describe("Stack", () => {
  it.fails("push and pop work correctly", () => {
    const s = new Stack<number>();
    s.push(1);
    s.push(2);
    expect(s.pop()).toBe(2);
    expect(s.pop()).toBe(1);
  });

  it.fails("peek returns top without removing", () => {
    const s = new Stack<number>();
    s.push(42);
    expect(s.peek()).toBe(42);
    expect(s.peek()).toBe(42); // still there
  });

  it.fails("isEmpty works correctly", () => {
    const s = new Stack<number>();
    expect(s.isEmpty()).toBe(true);
    s.push(1);
    expect(s.isEmpty()).toBe(false);
  });

  it.fails("pop empty returns undefined", () => {
    const s = new Stack<number>();
    expect(s.pop()).toBeUndefined();
  });
});

describe("validParentheses", () => {
  it.fails("returns true for valid simple", () => {
    expect(validParentheses("()")).toBe(true);
    expect(validParentheses("()[]{}")).toBe(true);
  });

  it.fails("returns true for valid nested", () => {
    expect(validParentheses("{[()]}")).toBe(true);
  });

  it.fails("returns false for invalid", () => {
    expect(validParentheses("(]")).toBe(false);
    expect(validParentheses("([)]")).toBe(false);
  });

  it.fails("returns true for empty string", () => {
    expect(validParentheses("")).toBe(true);
  });
});

describe("evaluatePostfix", () => {
  it.fails("evaluates simple addition", () => {
    expect(evaluatePostfix(["2", "3", "+"])).toBe(5);
  });

  it.fails("evaluates simple multiplication", () => {
    expect(evaluatePostfix(["2", "3", "*"])).toBe(6);
  });

  it.fails("evaluates complex expression", () => {
    expect(evaluatePostfix(["2", "1", "+", "3", "*"])).toBe(9);
  });

  it.fails("evaluates division", () => {
    expect(evaluatePostfix(["4", "2", "/"])).toBe(2);
  });
});

describe("MinStack", () => {
  it.fails("gets min correctly", () => {
    const s = new MinStack();
    s.push(3);
    s.push(1);
    s.push(2);
    expect(s.getMin()).toBe(1);
  });

  it.fails("updates min after pop", () => {
    const s = new MinStack();
    s.push(2);
    s.push(1);
    s.pop();
    expect(s.getMin()).toBe(2);
  });

  it.fails("handles duplicates correctly", () => {
    const s = new MinStack();
    s.push(1);
    s.push(1);
    s.pop();
    expect(s.getMin()).toBe(1);
  });
});
