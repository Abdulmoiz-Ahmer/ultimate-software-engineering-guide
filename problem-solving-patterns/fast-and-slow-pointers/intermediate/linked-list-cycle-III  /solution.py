# The first input of the test case is an array of values representing a linked list. 
# The second input is the index where the tail connects to form a cycle (or −1 if there's no cycle). 
# This index is used only to construct the linked list and is not passed to the function.

# Definition for a Linked List node:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

from ds_v1.LinkedList.LinkedList import ListNode

def count_cycle_length(head):
    # Initialize two pointers for Floyd's Cycle Detection Algorithm
    slow = fast = head
    
    # Traverse the linked list until fast reaches the end
    # or a cycle is detected
    while fast and fast.next:
        
        # Move slow pointer by 1 step
        slow = slow.next
        # Move fast pointer by 2 steps
        fast = fast.next.next
       
        # If slow and fast meet, a cycle is detected
        if slow == fast:
            # Move slow pointer by 1 step to start counting the cycle length
            slow = slow.next
            length = 1
           
            # Keep moving slow until it meets fast again
            # Increment length for each step
            while slow != fast:
                length += 1
                slow = slow.next
            
            # Return the length of the cycle
            return length   

    # If no cycle is found, return 0
    return 0
