# Solution: Longest Repeating Character Replacement

## Statement

Given a string `s` and an integer `k`, find the length of the **longest substring** in `s` where all characters are identical, after replacing **at most `k` characters** with any other uppercase English character.

---

## Constraints

- `1 ≤ s.length ≤ 10^3`
- `s` consists of only uppercase English characters (`A`–`Z`)
- `0 ≤ k ≤ s.length`

---

## Solution

So far, you’ve probably brainstormed some approaches and have an idea of how to solve this problem. Let’s explore some of these approaches and figure out which one to follow based on considerations such as time complexity and implementation constraints.

---

### Naive Approach

A brute force method checks every possible substring to see if it can be transformed into a string of identical characters with at most `k` replacements. Here’s how it works:

1. For each character in the string, consider every substring starting from that character.
2. For each substring, use a nested loop to count the number of replacements needed to make all its characters identical.
3. If the number of replacements is within the allowed limit `k` and the substring is longer than any previously found valid substring, update the longest length.

This method uses **three nested loops**—one to choose the starting point, one to choose the ending point, and one to calculate the required replacements—resulting in a time complexity of O(n^3) where `n` is the length of the input string.

### Optimized Approach Using Sliding Window

We need to find the maximum length of a substring where we can replace up to `k` characters to make all characters in the substring identical.

To solve this efficiently, we use the **sliding window** approach. It involves two pointers marking the start and end of a segment that moves across the main string. This method helps to quickly adjust the segment by expanding and contracting the window without repeatedly examining the same characters.

---

#### How It Works

1. **Initialize key variables:**

   - `lengthOfMaxSubstring` → stores the length of the longest valid substring found (initially `0`).
   - `start` → marks the left boundary of the sliding window (initially `0`).
   - `charFreq` → a frequency map that tracks how many times each character appears in the current window.
   - `mostFreqChar` → tracks the maximum frequency of any character within the current window (initially `0`).

2. **Iterate through the string using a pointer `end`:**

   - Take the character at position `end`.
   - Update its frequency in `charFreq`:
     - If it’s not in the map, set it to `1`.
     - If it exists, increment it by `1`.
   - Update `mostFreqChar` to the maximum of its current value and the frequency of the current character.

3. **Check window validity:**

   - The window is invalid if the number of replacements needed exceeds `k`:
     ```
     (end - start + 1) - mostFreqChar > k
     ```
   - If invalid:
     - Decrease the frequency of the character at position `start` in `charFreq`.
     - Move `start` forward by one position to shrink the window.

4. **Update result:**

   - After each iteration, update `lengthOfMaxSubstring` with the maximum valid window size:
     ```
     lengthOfMaxSubstring = max(lengthOfMaxSubstring, end - start + 1)
     ```

5. **Return the result:**
   - Once the loop finishes, `lengthOfMaxSubstring` contains the length of the longest valid substring.

### Time and Space Complexity

- **Time Complexity:** `O(n)` — each character is processed at most twice (once when expanding, once when shrinking).
- **Space Complexity:** `O(1)` — since there are only 26 uppercase English letters.

---

### Example

```text
Input:  s = "AABABBA", k = 1
Output: 4
Explanation:
Replace one 'A' in the middle to get "AABBBBA" → longest repeating substring = "BBBB"
```
