# Solution: Circular Array Loop

## Problem Statement

There is a **circular list** of non-zero integers called `nums`.  
Each number in the list tells you how many steps to move forward or backward from your current position:

- If `nums[i]` is **positive**, move `nums[i]` steps forward.
- If `nums[i]` is **negative**, move `nums[i]` steps backward.

### Circular Wrapping Rules:

- Moving forward from the last element takes you back to the first element.
- Moving backward from the first element takes you to the last element.

### Definition of a Valid Cycle:

A cycle in this list means:

1. You keep moving according to the numbers, and you end up repeating a sequence of indices.
2. All numbers in the cycle have the **same sign** (either all positive or all negative).
3. The cycle length is **greater than 1** (it involves at least two indices).

**Return `true`** if such a cycle exists in the list, otherwise return **`false`**.

---

## Constraints

- `1 ≤ nums.length ≤ 10^3`
- `-5000 ≤ nums[i] ≤ 5000`
- `nums[i] != 0`

---

## Naive Approach

- Iterate through each element of the array.
- For each element:
  - Start moving forward or backward as per the current value.
  - Use an additional array to track visited elements.
  - If a cycle is detected, return `true`.
  - If direction changes at any point, skip to the next element.

**Complexity:**

- **Time:** `O(n^2)` — Outer loop over each element, inner loop checks potential cycles.
- **Space:** `O(n)` — For the visited tracking array.

This approach is **inefficient** for large arrays.

---

## Optimized Approach: Fast and Slow Pointers

We use **Floyd's Cycle Detection Algorithm** (Tortoise & Hare) to efficiently detect cycles.

### Key Ideas:

- Maintain two pointers:
  - **Slow pointer:** Moves 1 step at a time.
  - **Fast pointer:** Moves 2 steps at a time.
- Both pointers must keep moving in the **same direction** (all positive or all negative values).
- If either pointer encounters:

  - A **direction change** (sign mismatch), or
  - A **self-loop** (value % size == 0),

  then we break and try the next starting index.

- If `slow` and `fast` meet, we found a cycle.

---

### Algorithm Workflow

For each index `i` in `nums`:

1. Initialize:
   - `slow = i`
   - `fast = i`
   - `direction = forward` if `nums[i] > 0` else `backward`
2. Move:
   - Slow pointer by **1 step**.
   - Fast pointer by **2 steps** (one step twice).
3. After each move, check:
   - **Direction validity:** sign of value must remain consistent.
   - **No self-loop:** `(value % size) != 0`.
4. If `slow == fast`, a valid cycle exists → **return `true`**.
5. If no valid cycle is found for any index → **return `false`**.

---

## Solution Summary

1. For each element of the array:
   - Move slow pointer `x` steps (value at current index).
   - Move fast pointer `x` steps, then `y` steps (value at the index reached after first move).
2. Return `true` if both pointers meet.
3. If movement direction changes, skip to the next element.
4. If no loop is found after checking all elements, return `false`.

---

## Time Complexity

- **Outer loop:** `O(n)`
- **Inner while loop:** Up to `O(n)` in the worst case.
- **Overall:** `O(n^2)`

## Space Complexity

- **O(1)** — No extra data structures used.

---
