import { assertEquals } from "@std/assert";
import { binarySearch } from "./main.ts";

Deno.test(function testBinarySearch() {
  let arr = [];
  let array = [0, 1, 2, 3, 4, 5, 6, 77];
  assertEquals(binarySearch(array, 77), 7);
  assertEquals(binarySearch(array, 770), -1);
  assertEquals(binarySearch(array, 0), 0);
});
