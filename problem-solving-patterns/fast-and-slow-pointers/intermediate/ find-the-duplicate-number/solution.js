export function findDuplicate(nums) {
  // Initialize slow and fast pointers to the starting index (0)
  let slow, fast;
  slow = fast = 0;

  // Phase 1: Detect the cycle
  // Treat the array as a linked list where nums[i] is the "next" pointer
  while (true) {
    slow = nums[slow]; // Move slow pointer by 1 step
    fast = nums[nums[fast]]; // Move fast pointer by 2 steps

    // If slow and fast meet, a cycle is detected
    if (slow === fast) {
      break;
    }
  }

  // Phase 2: Find the entry point of the cycle
  // Reset slow to the start of the list
  slow = 0;

  // Move both pointers one step at a time
  // They will meet at the duplicate number (start of the cycle)
  while (slow !== fast) {
    slow = nums[slow];
    fast = nums[fast];
  }

  // Return the duplicate number
  return fast;
}
