def longest_repeating_character_replacement(s, k):
    # Initialize pointers for the sliding window
    start = 0          # Left boundary of the window
    end = 0            # Right boundary of the window

    # Trackers for result and current state
    longest_repeating_substring = 0                       # Stores the maximum length found so far
    most_frequent_character_in_current_substring = 0      # Tracks the frequency of the most common character in the current window

    # Frequency dictionary to count characters in the current window
    char_frequency = {}

    # Expand the window by moving 'end' until it reaches the end of the string
    while end < len(s):
        # Increment the frequency of the current character
        if not char_frequency.get(s[end]):
            char_frequency[s[end]] = 1
        else:
            char_frequency[s[end]] = char_frequency.get(s[end]) + 1

        # Update the count of the most frequent character in the current window
        most_frequent_character_in_current_substring = max(
            most_frequent_character_in_current_substring, 
            char_frequency.get(s[end])
        )

        # Check if the current window is still valid
        # A window is invalid if we need more than k replacements
        if (end - start + 1) - most_frequent_character_in_current_substring > k:
            # Shrink the window from the left
            char_frequency[s[start]] = char_frequency.get(s[start]) - 1
            start = start + 1

        # Update the maximum valid window size
        longest_repeating_substring = max(
            end - start + 1, 
            longest_repeating_substring
        )

        # Move the window forward
        end = end + 1

    # Return the length of the longest valid substring found
    return longest_repeating_substring
