/**
 * Detects if a circular array contains a valid cycle.
 *
 * A valid cycle must:
 * - Move in a single direction (all positive or all negative values).
 * - Have a length greater than 1 (no self-loops).
 * - Wrap around the array in a circular manner.
 *
 * Uses Floyd's Cycle Detection (Tortoise and Hare) algorithm.
 *
 * @param {number[]} nums - The circular array of step sizes (positive = forward, negative = backward).
 * @returns {boolean} True if a valid cycle exists, false otherwise.
 */
function circularArrayLoop(nums) {
  const size = nums.length;

  // Try starting from each index in the array
  for (let i = 0; i < size; i++) {
    let slow = i; // Slow pointer (moves 1 step at a time)
    let fast = i; // Fast pointer (moves 2 steps at a time)

    // Determine initial movement direction
    let direction = nums[i] > 0 ? "forward" : "backward";

    while (true) {
      // Move slow pointer 1 step
      slow = movePointer(nums[slow], slow, size);
      if (invalidCycle(nums[slow], direction, size)) {
        break; // Stop if invalid move
      }

      // Move fast pointer 1 step
      fast = movePointer(nums[fast], fast, size);
      if (invalidCycle(nums[fast], direction, size)) {
        break; // Stop if invalid move
      }

      // Move fast pointer 1 more step (total 2 steps this loop)
      fast = movePointer(nums[fast], fast, size);
      if (invalidCycle(nums[fast], direction, size)) {
        break; // Stop if invalid move
      }

      // If slow and fast pointers meet, a cycle exists
      if (slow === fast) {
        return true;
      }
    }
  }
  // No cycle found
  return false;
}

/**
 * Checks if the current movement breaks the cycle rules.
 *
 * @param {number} value - The current array value (step size and direction).
 * @param {string} direction - The expected movement direction ("forward" or "backward").
 * @param {number} size - The size of the array.
 * @returns {boolean} True if movement is invalid.
 */
function invalidCycle(value, direction, size) {
  const newDirection = value > 0 ? "forward" : "backward";

  // Invalid if direction changes or if value causes a self-loop
  if (direction !== newDirection || value % size === 0) {
    return true;
  }
  return false;
}

/**
 * Moves the pointer in the array based on the given step value.
 * Wraps around circularly for both forward and backward moves.
 *
 * @param {number} value - The number of steps to move (positive or negative).
 * @param {number} pointer - The current index position.
 * @param {number} size - The size of the array.
 * @returns {number} The new index position after moving.
 */
function movePointer(value, pointer, size) {
  let result = (pointer + value) % size;

  // Wrap negative results to the end of the array
  if (result < 0) result += size;

  return result;
}

export { circularArrayLoop };
