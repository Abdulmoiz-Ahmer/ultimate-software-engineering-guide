# Solution: Find The Duplicate Number

## Statement

Given an array of positive numbers `nums`, where values are in the range `[1, n]` (inclusive), and there are `n + 1` elements in the array, find and return the duplicate number.

There is exactly **one repeated number** in `nums`, which may appear more than once.

**Note:**

- You cannot modify the array `nums`.
- The solution must use only **constant extra space**.

---

## Constraints

- `1 ≤ n ≤ 10^3`
- `nums.length = n + 1`
- `1 ≤ nums[i] ≤ n`
- All integers in `nums` are unique **except** for one that repeats.

---

## Approach

This problem can be solved using **Floyd’s Tortoise and Hare algorithm** in two phases:

### 1. Detect the Cycle

Treat the array like a linked list where each index points to `nums[index]`.

- Use a `slow` pointer that moves one step at a time.
- Use a `fast` pointer that moves two steps at a time.
- Both start at index `0`.
- Eventually, the two pointers will meet inside a cycle caused by the duplicate number.

### 2. Find the Start of the Cycle (Duplicate Number)

- Reset `slow` to index `0` while keeping `fast` at the meeting point.
- Move both pointers one step at a time.
- The point where they meet again is the duplicate number.

---

## Why This Works

The duplicate number causes two indices to point to the same next index, forming a cycle.
By detecting and finding the entry point of the cycle, we identify the duplicate number without modifying the array or using extra space.
