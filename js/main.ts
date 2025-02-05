export function binarySearch(array: Array<number>, find: number): number {
  let left = 0;
  let right = array.length - 1;
  let mid;
  while (left <= right) {
    mid = Math.floor((left + right) / 2);
    if (array[mid] > find) {
      right = mid - 1;
    } else if (array[mid] < find) {
      left = mid + 1;
    } else {
      return mid;
    }
  }
  return -1;
}
// Learn more at https://docs.deno.com/runtime/manual/examples/module_metadata#concepts
if (import.meta.main) {
  console.log("Hello");
}
