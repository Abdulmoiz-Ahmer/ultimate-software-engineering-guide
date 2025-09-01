# Challenge: Mediator Pattern

## Problem Statement

In this challenge, you need to use the mediator pattern to implement the HR of an office that mediates between the employees (workers and managers) of a company.

You have been given the dummy code for the **HR** class. You need to define its **constructor** and the functions:

- **registerEmployee(employee)**: Registers an employee

- **scheduleRaise(raise, worker, manager)**: Conveys the raise to the manager. Once the manager approves the raise, it gives the raise to the worker

Now, let’s look at the **Manager** and **Worker** classes. Both of them inherit from the **Employee** class (already defined for you). You need to do the following:

- Define the **constructor** for both classes

- In **Manager** class, define the **receiveMessage** function. It should display the message received from the HR regarding the salary raise of the worker

- In **Manager** class, define the **approveRaise** function. It should display a message of approval of the raise and return true after approval

- In the **Worker** class, define the **receiveRaise** function. It should increment the worker’s pay by the raise and display a message for the new pay

---

## Input

The **scheduleRaise** function is called

## Output

The messages conveying the raise to the manager, manager approving the raise, and the final pay are displayed

---

## Sample Input

```javascript
var hr = new HR();
var employee = new Worker(hr, "Joe", "Developer", 1400);
var manager = new Manager(hr, "Allen", "Team Lead", 3000);
hr.scheduleRaise(200, employee, manager);
```

## Sample Output

```javascript
"Joe should get 200 dollar raise"; //HR conveying the message to the manager
"Joe's 200 dollar raise is approved"; //manager approving the raise
"My new pay is 1600 dollars"; //worker announcing the new pay
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class HR {
  //initialize the constructor here
  constructor() {
    //define the constructor
  }

  registerEmployee(employee) {
    //write-code-here
  }

  scheduleRaise(raise, worker, manager) {
    //write-code-here
  }
}

class Employee {
  constructor(hr, name, position, pay) {
    this.hr = hr;
    this.name = name;
    this.position = position;
    this.pay = pay;
  }
}

class Manager extends Employee {
  //initialize the constructor here
  constructor() {
    //define the constructor
  }
  receiveMessage(worker, raise) {
    //write your code here
  }
  finalizeRaise(worker, raise) {
    //write your code here
  }
}

class Worker extends Employee {
  //initialize the constructor here
  constructor() {
    //define the constructor
  }
  receiveRaise(raise) {
    //write your code here
  }
}
```
