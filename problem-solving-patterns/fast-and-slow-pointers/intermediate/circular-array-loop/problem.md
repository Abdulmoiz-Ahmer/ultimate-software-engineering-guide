# Problem: Circular Array Loop

## Statement

You are given a **circular list** of **non-zero integers** called `nums`.  
Each number in the list tells you how many steps to move **forward** or **backward** from your current position:

- If `nums[i]` is **positive**, move `nums[i]` steps forward.
- If `nums[i]` is **negative**, move `nums[i]` steps backward.

Since the list is **circular**:

- Moving forward from the last element wraps around to the first element.
- Moving backward from the first element wraps around to the last element.

A **cycle** in this list means:

1. You keep moving according to the numbers, and eventually repeat a sequence of indices.
2. **All numbers** in the cycle have the **same sign** (either all positive or all negative).
3. The **cycle length** is **greater than 1** (involves at least two indices).

Return **`true`** if such a cycle exists in the list, otherwise **`false`**.

---

## Constraints

- `1 ≤ nums.length ≤ 10^3`
- `-5000 ≤ nums[i] ≤ 5000`
- `nums[i] != 0`

---
