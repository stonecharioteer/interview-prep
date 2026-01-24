import { describe, it, expect } from "vitest";
import { Queue, QueueUsingStacks } from "../../src/2026/queue.js";

describe("Queue", () => {
  it.fails("enqueue and dequeue work FIFO", () => {
    const q = new Queue<number>();
    q.enqueue(1);
    q.enqueue(2);
    expect(q.dequeue()).toBe(1);
    expect(q.dequeue()).toBe(2);
  });

  it.fails("peek returns front without removing", () => {
    const q = new Queue<number>();
    q.enqueue(42);
    expect(q.peek()).toBe(42);
    expect(q.peek()).toBe(42); // still there
  });

  it.fails("isEmpty works correctly", () => {
    const q = new Queue<number>();
    expect(q.isEmpty()).toBe(true);
    q.enqueue(1);
    expect(q.isEmpty()).toBe(false);
  });

  it.fails("dequeue empty returns undefined", () => {
    const q = new Queue<number>();
    expect(q.dequeue()).toBeUndefined();
  });
});

describe("QueueUsingStacks", () => {
  it.fails("maintains FIFO order", () => {
    const q = new QueueUsingStacks<number>();
    q.enqueue(1);
    q.enqueue(2);
    q.enqueue(3);
    expect(q.dequeue()).toBe(1);
    expect(q.dequeue()).toBe(2);
    expect(q.dequeue()).toBe(3);
  });

  it.fails("handles interleaved operations", () => {
    const q = new QueueUsingStacks<number>();
    q.enqueue(1);
    q.enqueue(2);
    expect(q.dequeue()).toBe(1);
    q.enqueue(3);
    expect(q.dequeue()).toBe(2);
    expect(q.dequeue()).toBe(3);
  });

  it.fails("dequeue empty returns undefined", () => {
    const q = new QueueUsingStacks<number>();
    expect(q.dequeue()).toBeUndefined();
  });
});
