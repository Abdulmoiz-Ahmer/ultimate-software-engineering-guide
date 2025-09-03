# Challenge: Builder Pattern

In this challenge, you have to complete the implementation of the code after studying the partial code.

The task here is to implement the builder pattern to create an assignment. Each assignment has:

- A subject
- A level (easy, medium, or hard)
- A due date

The `announcement` function given to you displays all this information. You have to:

1. Figure out where to put this function's definition
2. Implement how to build the assignment step-by-step

## Input

The provided partial code

## Output

Complete implementation of the code and the result after calling the `announcement` method

## Sample Input

```javascript
mathAssignment.announcement();
```

## Sample Output

```javascript
"Your Math assignment is: Hard. It is due on 12th June, 2020.";
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the provided solution. Good luck!

```javascript
//write-your-code-implementation-here

//figure out where you need to put this method
this.announcement = function () {
  console.log(
    `Your ${this.subject} assignment's difficulty level is: ${this.level}. It is due on ${this.dueDate}.`
  );
};

try {
  var assignment = new Assignment();
  var assignmentBuilder = new AssignmentBuilder(
    "Math",
    "Hard",
    "12th June, 2020"
  );
  var mathAssignment = assignment.make(assignmentBuilder);
  mathAssignment.announcement();
} catch (e) {
  console.log(e);
}
```
