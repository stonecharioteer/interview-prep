/**
 * Linked list operations for DSA practice.
 */

export class ListNode<T = number> {
  constructor(
    public value: T,
    public next: ListNode<T> | null = null
  ) {}

  /** Convert linked list to array */
  toArray(): T[] {
    const result: T[] = [];
    let current: ListNode<T> | null = this;
    while (current) {
      result.push(current.value);
      current = current.next;
    }
    return result;
  }
}

/** Create linked list from array of values */
export function fromArray<T>(values: T[]): ListNode<T> | null {
  if (values.length === 0) return null;
  const head = new ListNode(values[0]);
  let current = head;
  for (let i = 1; i < values.length; i++) {
    current.next = new ListNode(values[i]);
    current = current.next;
  }
  return head;
}

/** Generate random linked list of given size */
export function getRandomList(size: number): ListNode<number> {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Find maximum value in linked list */
export function getMax(head: ListNode<number>): number {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Find minimum value in linked list */
export function getMin(head: ListNode<number>): number {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Calculate sum of all values */
export function getSum(head: ListNode<number>): number {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Check if value exists in list */
export function contains(head: ListNode<number>, n: number): boolean {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Get length of linked list */
export function getLength(head: ListNode | null): number {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Calculate average of values */
export function getAverage(head: ListNode<number>): number {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Count occurrences of a value */
export function countOf(head: ListNode<number>, n: number): number {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Get value at index k (0-based) */
export function getKth(head: ListNode<number>, k: number): number | null {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Append value to end of list */
export function append(head: ListNode<number>, value: number): ListNode<number> {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Prepend value to beginning of list */
export function prepend(head: ListNode<number> | null, value: number): ListNode<number> {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Remove first occurrence of value */
export function removeFirst(head: ListNode<number>, value: number): ListNode<number> | null {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Insert value at given index */
export function insertAtIndex(
  head: ListNode<number> | null,
  index: number,
  value: number
): ListNode<number> {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Remove node at given index */
export function removeAtIndex(head: ListNode<number>, index: number): ListNode<number> | null {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Reverse linked list iteratively */
export function reverse(head: ListNode<number> | null): ListNode<number> | null {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Find middle node (second middle for even length) */
export function getMiddle(head: ListNode<number>): ListNode<number> {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Detect if list has a cycle (Floyd's algorithm) */
export function hasCycle(head: ListNode<number> | null): boolean {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Merge two sorted linked lists */
export function mergeSorted(
  a: ListNode<number> | null,
  b: ListNode<number> | null
): ListNode<number> | null {
  // TODO: Implement
  throw new Error("Not implemented");
}

/** Get nth node from end (1-indexed) */
export function getNthFromEnd(head: ListNode<number>, n: number): number | null {
  // TODO: Implement
  throw new Error("Not implemented");
}
