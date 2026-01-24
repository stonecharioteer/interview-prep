import { describe, it, expect } from "vitest";
import * as ll from "../../src/2026/linkedList.js";

// Helper to create list from values
const createList = (values: number[]) => ll.fromArray(values);

describe("ListNode", () => {
  it("creates node with value", () => {
    const node = new ll.ListNode(10);
    expect(node.value).toBe(10);
    expect(node.next).toBeNull();
  });

  it("creates node with child", () => {
    const child = new ll.ListNode(20);
    const parent = new ll.ListNode(10, child);
    expect(parent.next).toBe(child);
    expect(parent.next?.value).toBe(20);
  });

  it("converts to array", () => {
    const list = createList([1, 2, 3, 4, 5]);
    expect(list?.toArray()).toEqual([1, 2, 3, 4, 5]);
  });
});

describe("getMax", () => {
  it.fails("finds max in simple list", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.getMax(list)).toBe(5);
  });

  it.fails("finds max in single node", () => {
    const list = createList([42])!;
    expect(ll.getMax(list)).toBe(42);
  });

  it.fails("finds max with negatives", () => {
    const list = createList([-10, 5, -3, 0, -7])!;
    expect(ll.getMax(list)).toBe(5);
  });

  it.fails("finds max at different positions", () => {
    expect(ll.getMax(createList([100, 1, 2, 3])!)).toBe(100);
    expect(ll.getMax(createList([1, 2, 3, 100])!)).toBe(100);
    expect(ll.getMax(createList([1, 100, 2, 3])!)).toBe(100);
  });
});

describe("getMin", () => {
  it.fails("finds min in simple list", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.getMin(list)).toBe(1);
  });

  it.fails("finds min with negatives", () => {
    const list = createList([-10, 5, -3, 0, -7])!;
    expect(ll.getMin(list)).toBe(-10);
  });

  it.fails("finds min at different positions", () => {
    expect(ll.getMin(createList([1, 10, 20, 30])!)).toBe(1);
    expect(ll.getMin(createList([10, 20, 30, 1])!)).toBe(1);
    expect(ll.getMin(createList([10, 1, 20, 30])!)).toBe(1);
  });
});

describe("getSum", () => {
  it.fails("sums simple list", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.getSum(list)).toBe(15);
  });

  it.fails("sums single node", () => {
    const list = createList([42])!;
    expect(ll.getSum(list)).toBe(42);
  });

  it.fails("sums to zero", () => {
    const list = createList([5, -5, 10, -10])!;
    expect(ll.getSum(list)).toBe(0);
  });
});

describe("contains", () => {
  it.fails("finds existing element", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.contains(list, 3)).toBe(true);
  });

  it.fails("returns false for missing", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.contains(list, 999)).toBe(false);
  });
});

describe("getLength", () => {
  it.fails("gets length of list", () => {
    expect(ll.getLength(createList([1, 2, 3, 4, 5]))).toBe(5);
  });

  it.fails("handles single node", () => {
    expect(ll.getLength(createList([42]))).toBe(1);
  });

  it.fails("handles null", () => {
    expect(ll.getLength(null)).toBe(0);
  });
});

describe("getAverage", () => {
  it.fails("calculates average", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.getAverage(list)).toBe(3);
  });

  it.fails("handles single node", () => {
    const list = createList([42])!;
    expect(ll.getAverage(list)).toBe(42);
  });
});

describe("countOf", () => {
  it.fails("counts existing element", () => {
    const list = createList([5, 3, 5, 7, 5, 3])!;
    expect(ll.countOf(list, 5)).toBe(3);
    expect(ll.countOf(list, 3)).toBe(2);
    expect(ll.countOf(list, 7)).toBe(1);
  });

  it.fails("returns zero for missing", () => {
    const list = createList([1, 2, 3])!;
    expect(ll.countOf(list, 99)).toBe(0);
  });
});

describe("getKth", () => {
  it.fails("gets items at valid indices", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.getKth(list, 0)).toBe(1);
    expect(ll.getKth(list, 2)).toBe(3);
    expect(ll.getKth(list, 4)).toBe(5);
  });

  it.fails("returns null for out of bounds", () => {
    const list = createList([1, 2, 3])!;
    expect(ll.getKth(list, 100)).toBeNull();
  });
});

describe("append", () => {
  it.fails("appends to single node", () => {
    const list = createList([1])!;
    const result = ll.append(list, 2);
    expect(result.toArray()).toEqual([1, 2]);
  });

  it.fails("appends multiple", () => {
    let list = createList([1])!;
    list = ll.append(list, 2);
    list = ll.append(list, 3);
    expect(list.toArray()).toEqual([1, 2, 3]);
  });
});

describe("prepend", () => {
  it.fails("prepends to single node", () => {
    const list = createList([2])!;
    const result = ll.prepend(list, 1);
    expect(result.toArray()).toEqual([1, 2]);
  });

  it.fails("prepends to null", () => {
    const result = ll.prepend(null, 1);
    expect(result.toArray()).toEqual([1]);
  });
});

describe("removeFirst", () => {
  it.fails("removes from middle", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    const result = ll.removeFirst(list, 3);
    expect(result?.toArray()).toEqual([1, 2, 4, 5]);
  });

  it.fails("removes head", () => {
    const list = createList([1, 2, 3])!;
    const result = ll.removeFirst(list, 1);
    expect(result?.toArray()).toEqual([2, 3]);
  });

  it.fails("removes tail", () => {
    const list = createList([1, 2, 3])!;
    const result = ll.removeFirst(list, 3);
    expect(result?.toArray()).toEqual([1, 2]);
  });

  it.fails("removes only first occurrence", () => {
    const list = createList([1, 2, 2, 3])!;
    const result = ll.removeFirst(list, 2);
    expect(result?.toArray()).toEqual([1, 2, 3]);
  });
});

describe("insertAtIndex", () => {
  it.fails("inserts at start", () => {
    const list = createList([2, 3, 4])!;
    const result = ll.insertAtIndex(list, 0, 1);
    expect(result.toArray()).toEqual([1, 2, 3, 4]);
  });

  it.fails("inserts in middle", () => {
    const list = createList([1, 2, 4, 5])!;
    const result = ll.insertAtIndex(list, 2, 3);
    expect(result.toArray()).toEqual([1, 2, 3, 4, 5]);
  });

  it.fails("inserts at end", () => {
    const list = createList([1, 2, 3])!;
    const result = ll.insertAtIndex(list, 3, 4);
    expect(result.toArray()).toEqual([1, 2, 3, 4]);
  });

  it.fails("inserts into empty", () => {
    const result = ll.insertAtIndex(null, 0, 1);
    expect(result.toArray()).toEqual([1]);
  });
});

describe("removeAtIndex", () => {
  it.fails("removes at start", () => {
    const list = createList([1, 2, 3])!;
    const result = ll.removeAtIndex(list, 0);
    expect(result?.toArray()).toEqual([2, 3]);
  });

  it.fails("removes in middle", () => {
    const list = createList([1, 2, 3, 4])!;
    const result = ll.removeAtIndex(list, 2);
    expect(result?.toArray()).toEqual([1, 2, 4]);
  });

  it.fails("removes single element", () => {
    const list = createList([1])!;
    const result = ll.removeAtIndex(list, 0);
    expect(result).toBeNull();
  });
});

describe("reverse", () => {
  it.fails("reverses simple list", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    const result = ll.reverse(list);
    expect(result?.toArray()).toEqual([5, 4, 3, 2, 1]);
  });

  it.fails("reverses two elements", () => {
    const list = createList([1, 2])!;
    const result = ll.reverse(list);
    expect(result?.toArray()).toEqual([2, 1]);
  });

  it.fails("reverses single element", () => {
    const list = createList([42])!;
    const result = ll.reverse(list);
    expect(result?.toArray()).toEqual([42]);
  });

  it.fails("handles null", () => {
    expect(ll.reverse(null)).toBeNull();
  });
});

describe("getMiddle", () => {
  it.fails("finds middle of odd length", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.getMiddle(list).value).toBe(3);
  });

  it.fails("finds second middle of even length", () => {
    const list = createList([1, 2, 3, 4])!;
    expect(ll.getMiddle(list).value).toBe(3);
  });

  it.fails("finds middle of single element", () => {
    const list = createList([42])!;
    expect(ll.getMiddle(list).value).toBe(42);
  });
});

describe("hasCycle", () => {
  it.fails("returns false for no cycle", () => {
    const list = createList([1, 2, 3, 4, 5]);
    expect(ll.hasCycle(list)).toBe(false);
  });

  it.fails("detects cycle to head", () => {
    const list = createList([1, 2, 3])!;
    let current = list;
    while (current.next) current = current.next;
    current.next = list;
    expect(ll.hasCycle(list)).toBe(true);
  });

  it.fails("detects cycle to middle", () => {
    const list = createList([1, 2, 3, 4])!;
    const second = list.next!;
    let current = list;
    while (current.next) current = current.next;
    current.next = second;
    expect(ll.hasCycle(list)).toBe(true);
  });

  it.fails("handles single node without cycle", () => {
    const list = createList([1]);
    expect(ll.hasCycle(list)).toBe(false);
  });

  it.fails("handles null", () => {
    expect(ll.hasCycle(null)).toBe(false);
  });
});

describe("mergeSorted", () => {
  it.fails("merges two lists", () => {
    const a = createList([1, 3, 5]);
    const b = createList([2, 4, 6]);
    const result = ll.mergeSorted(a, b);
    expect(result?.toArray()).toEqual([1, 2, 3, 4, 5, 6]);
  });

  it.fails("handles empty first", () => {
    const b = createList([1, 2, 3]);
    const result = ll.mergeSorted(null, b);
    expect(result?.toArray()).toEqual([1, 2, 3]);
  });

  it.fails("handles empty second", () => {
    const a = createList([1, 2, 3]);
    const result = ll.mergeSorted(a, null);
    expect(result?.toArray()).toEqual([1, 2, 3]);
  });

  it.fails("handles both empty", () => {
    expect(ll.mergeSorted(null, null)).toBeNull();
  });

  it.fails("handles duplicates", () => {
    const a = createList([1, 2, 2]);
    const b = createList([2, 3, 3]);
    const result = ll.mergeSorted(a, b);
    expect(result?.toArray()).toEqual([1, 2, 2, 2, 3, 3]);
  });
});

describe("getNthFromEnd", () => {
  it.fails("gets first from end", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.getNthFromEnd(list, 1)).toBe(5);
  });

  it.fails("gets second from end", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.getNthFromEnd(list, 2)).toBe(4);
  });

  it.fails("gets last from end (first element)", () => {
    const list = createList([1, 2, 3, 4, 5])!;
    expect(ll.getNthFromEnd(list, 5)).toBe(1);
  });

  it.fails("returns null for out of bounds", () => {
    const list = createList([1, 2, 3])!;
    expect(ll.getNthFromEnd(list, 10)).toBeNull();
  });
});
