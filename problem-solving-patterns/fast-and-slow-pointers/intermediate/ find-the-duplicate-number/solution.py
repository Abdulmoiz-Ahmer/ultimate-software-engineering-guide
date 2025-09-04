def find_duplicate(nums):
    # Initialize both slow and fast pointers to the start index (0)
    slow = 0
    fast = 0 
    
    # Phase 1: Detect a cycle using Floyd's Tortoise and Hare algorithm
    while True:
        slow = nums[slow]              # Move slow pointer by 1 step
        fast = nums[nums[fast]]        # Move fast pointer by 2 steps
        
        if slow == fast:               # Cycle detected (pointers meet)
            break

    # Phase 2: Find the entrance to the cycle (duplicate number)
    slow = 0                           # Reset slow pointer to start
    while slow != fast:
        slow = nums[slow]              # Move slow pointer by 1 step
        fast = nums[fast]              # Move fast pointer by 1 step
    
    return fast                        # The meeting point is the duplicate
