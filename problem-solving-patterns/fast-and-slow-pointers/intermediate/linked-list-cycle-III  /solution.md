# Solution: Linked List Cycle III

## Statement

Given the head of a linked list, determine the length of the cycle present in the linked list. If there is no cycle, return `0`.

A cycle exists in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer.

**Constraints:**

- The number of nodes in the list is in the range **[0, 10⁴]**.
- **−10⁵ ≤ Node.value ≤ 10⁵**

---

## Solution

The **fast and slow pointers technique** is an efficient method for detecting cycles in a linked list.

- The **fast pointer** advances two steps at a time.
- The **slow pointer** moves one step at a time.

If the list has **no cycle**, the fast pointer will eventually reach the end (`NULL`) without meeting the slow pointer.  
However, if a cycle exists, the fast pointer will eventually catch up to the slow pointer, confirming the presence of a cycle.

Once the two pointers meet inside the cycle, this meeting point can be used to determine the cycle’s length:

1. Keep one pointer fixed at the meeting point.
2. Move the other pointer one step at a time through the cycle.
3. Count the steps until it returns to the meeting point — this is the **cycle length**.

---

## Steps of the Algorithm

1. **Initialize two pointers** (`fast` and `slow`) pointing at the linked list’s head.

2. **Detect the cycle**:

   - Move `slow` one step forward.
   - Move `fast` two steps forward.
   - If `fast` is `NULL` or `fast.next` is `NULL`, there is **no cycle** → return `0`.
   - If `slow` and `fast` meet, a cycle has been detected.

3. **Determine the length**:

   - Fix `fast` at the meeting point.
   - Move `slow` one step forward, set `length = 1`.
   - Continue moving `slow` until it meets `fast` again, incrementing `length` at each step.
   - When they meet again, return `length`.

4. If no cycle is found, return `0`.

---

## Time Complexity

- **O(n)** — Each pointer traverses the list at most twice.

## Space Complexity

- **O(1)** — Only constant extra space is used.
