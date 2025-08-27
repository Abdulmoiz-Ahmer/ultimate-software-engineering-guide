# Challenge: Chain of Responsibility Pattern

## Problem Statement

In this challenge, you have to use the chain of responsibility pattern to implement the functionality of assigning work to employees.

Each employee has a name and a level property. The level of an employee tells which task they can handle, that is, easy, medium, or hard. Hence, each employee is assigned a task depending on their level.

You have already been provided an abstract class **EmployeeChain**. It contains two functions:

- **setNextEmp**: sets the next object in the chain
- **assignWork**: assigns work to an employee depending on their level

You have to use the chain of responsibility pattern to implement these functions, so you can achieve the final goal of assigning work to employees.

---

## Input

Function **assignWork** is called to assign work to an employee

---

## Output

A message is displayed that the work has been assigned to the appropriate employee

---

## Sample Input

```javascript
var w1 = new EasyLevelWorkHandler();
var w2 = new MediumLevelWorkHandler();
var w3 = new HardLevelWorkHandler();
w1.setNextEmp(w2);
w2.setNextEmp(w3);

const emp1 = new Employee("Joe", "Easy");
const emp2 = new Employee("Anne", "Medium");
const emp3 = new Employee("Shawn", "Hard");

w1.assignWork(emp1);
w1.assignWork(emp2);
w1.assignWork(emp3);
```

## Sample Output

```javascript
"Easy work assigned to: Joe";
"Medium work assigned to: Anne";
"Hard work assigned to: Shawn";
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class EmployeeChain {
  setNextEmp(nextEmpInChain) {}
  assignWork(req) {}
}
```
