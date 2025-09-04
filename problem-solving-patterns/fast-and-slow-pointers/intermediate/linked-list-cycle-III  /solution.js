// The first input of the test case is an array of values representing a linked list.
// The second input is the index where the tail connects to form a cycle (or −1 if there's no cycle).
// This index is used only to construct the linked list and is not passed to the function.

// Definition for a Linked List node
// class ListNode {
//     constructor(val = 0, next = null) {
//         this.val = val;
//         this.next = next;
//     }
// }

import { ListNode } from "./ds_v1/LinkedList.js";

function countCycleLength(head) {
  // Initialize two pointers, both starting at the head
  let slow, fast;
  fast = slow = head;

  // Traverse the list while fast and fast.next are valid
  // This ensures we don't run into null pointers
  while (fast && fast.next) {
    // Move slow pointer by 1 step
    slow = slow.next;
    // Move fast pointer by 2 steps
    fast = fast.next.next;

    // If slow and fast meet, a cycle is detected
    if (slow === fast) {
      // Start counting cycle length
      let length = 1;
      // Move slow one step ahead to start measurement
      slow = slow.next;

      // Continue moving slow pointer until it meets fast again
      // Count the number of steps taken to complete the loop
      while (slow !== fast) {
        length++;
        slow = slow.next;
      }

      // Return the total cycle length
      return length;
    }
  }

  // If no cycle is found, return 0
  return 0;
}

export { countCycleLength };
