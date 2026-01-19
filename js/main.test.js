import assert from "node:assert/strict";
import test from "node:test";
import { binarySearch } from "./main.js";

test("binary search", () => {
  let array = [0, 1, 2, 3, 4, 5, 6, 77];
  assert.equal(binarySearch(array, 77), 7);
  assert.equal(binarySearch(array, 770), -1);
  assert.equal(binarySearch(array, 0), 0);
});
