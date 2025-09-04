def isNotValidCycle(direction, value, size):
    """
    Checks if the current step breaks the rules for forming a valid cycle.

    Args:
        direction (str): The expected movement direction ("forward" or "backward").
        value (int): The step size at the current position (positive or negative).
        size (int): The size of the array.

    Returns:
        bool: True if the movement is invalid because:
              1. The movement changes direction from the original.
              2. The step size results in no movement (value % size == 0).
    """
    newDirection = "forward" if value > 0 else "backward"

    # Invalid if direction changes OR if it forms a self-loop (no actual movement)
    if direction != newDirection or value % size == 0:
        return True
    return False


def movePointer(pointer, value, size):
    """
    Moves the pointer within the circular array.

    Args:
        pointer (int): The current index.
        value (int): The step size (positive for forward, negative for backward).
        size (int): The size of the array.

    Returns:
        int: The new index after applying the step, wrapped circularly.
    """
    # Wrap the movement using modulo
    result = (pointer + value) % size

    # If the result is negative after modulo, wrap it to the end
    if result < 0:
        result += size
    return result


def circular_array_loop(nums):
    """
    Determines if the circular array contains a valid cycle.

    Rules for a valid cycle:
    1. All movements in the cycle must have the same sign (all forward or all backward).
    2. Cycle length must be greater than 1 (no single-element loops).
    3. Movement is circular (wraps around the array).

    Uses Floyd's Cycle Detection Algorithm (Tortoise & Hare).

    Args:
        nums (List[int]): The circular array of step sizes.

    Returns:
        bool: True if a valid cycle exists, False otherwise.
    """
    size = len(nums)

    # Try starting from each index
    for i in range(size):
        slow = fast = i
        direction = "forward" if nums[i] > 0 else "backward"

        while True:
            # Move slow pointer by 1 step
            slow = movePointer(slow, nums[slow], size)
            if isNotValidCycle(direction, nums[slow], size):
                break

            # Move fast pointer by 1 step
            fast = movePointer(fast, nums[fast], size)
            if isNotValidCycle(direction, nums[fast], size):
                break

            # Move fast pointer by another step (total 2 steps)
            fast = movePointer(fast, nums[fast], size)
            if isNotValidCycle(direction, nums[fast], size):
                break

            # If pointers meet, a cycle is found
            if slow == fast:
                return True

    # No valid cycle found
    return False
