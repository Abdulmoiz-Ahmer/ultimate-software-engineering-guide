# Problem: Longest Repeating Character Replacement

## Statement

Given a string `s` and an integer `k`, find the length of the **longest substring** in `s` where all characters are identical, after replacing **at most `k` characters** with any other uppercase English character.

---

## Constraints

- `1 ≤ s.length ≤ 10^3`
- `s` consists of only uppercase English characters (`A`–`Z`)
- `0 ≤ k ≤ s.length`

---

## Example

```text
Input:  s = "AABABBA", k = 1
Output: 4
Explanation: Replace the one 'A' in the middle to get "AABBBBA" → longest repeating substring = "BBBB"
```
