/**
 * Finds the length of the longest substring that can be transformed into
 * a string with all identical characters by replacing at most 'k' characters.
 *
 * Example:
 * longestRepeatingCharacterReplacement("AABABBA", 1) -> 4
 *
 * Sliding Window Approach (O(n) time, O(1) space since alphabet is limited)
 */

function longestRepeatingCharacterReplacement(s, k) {
  // Initialize pointers and tracking variables
  let start = 0; // left boundary of window
  let end = 0; // right boundary of window
  let longestSubstringLength = 0; // stores result
  let mostFrequentCharacterInCurrentSubstring = 0; // max frequency in current window

  // Map to track character frequencies in the current window
  let charFreq = new Map();

  // Expand the window using the 'end' pointer
  while (end < s.length) {
    // Increment frequency of the current character
    if (!charFreq.has(s[end])) {
      charFreq.set(s[end], 1);
    } else {
      charFreq.set(s[end], charFreq.get(s[end]) + 1);
    }

    // Update the most frequent character count in the current window
    mostFrequentCharacterInCurrentSubstring = Math.max(
      mostFrequentCharacterInCurrentSubstring,
      charFreq.get(s[end])
    );

    /**
     * If replacements needed exceed 'k', shrink the window from the left.
     * (Window size - most frequent char count > k means too many changes required)
     */
    if (end - start + 1 - mostFrequentCharacterInCurrentSubstring > k) {
      charFreq.set(s[start], charFreq.get(s[start]) - 1);
      start++; // move the left boundary forward
    }

    // Update the result with the largest valid window size seen so far
    longestSubstringLength = Math.max(longestSubstringLength, end - start + 1);

    // Move the right boundary forward
    end++;
  }

  // Return the maximum length found
  return longestSubstringLength;
}

export { longestRepeatingCharacterReplacement };
