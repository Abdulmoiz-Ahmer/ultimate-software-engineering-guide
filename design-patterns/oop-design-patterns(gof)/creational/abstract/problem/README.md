# Challenge: Abstract Pattern

---

## Problem Statement

You are given the **abstract constructor function** `Loans`.  
There are three types of loans that can be given:

- `HomeLoan`
- `StudentLoan`
- `PersonalLoan`

Your task is to implement `Loans` so that it decides **which loan instance to instantiate** based on the input parameters.

---

## Function to Implement

Implement a function **`getLoan`** that takes the following parameters:

- `type`: Type of loan
- `amount`: Amount of the loan
- `duration`: Duration of the loan (in years)

---

## Loan Properties

All three loan types must have:

- `amount`: The amount of loan required (in dollars)
- `duration`: The duration of time (in years) for which the loan is borrowed
- `interest`: The annual interest rate

### Interest Rates:

- **HomeLoan**: `0.08`
- **StudentLoan**: `0.03`
- **PersonalLoan**: `0.05`

---

## Loan Method

Each loan type must define the method **`calculateInterest`** to calculate **simple interest**:

**Formula:**

```javascript
TotalInterest = amount * interest * duration;
```

---

## Input

The `calculateInterest` method called for the chosen loan.

---

## Output

The total interest on the money borrowed.

---

## Sample Input

```javascript
var loan = new Loans();

var homeLoan = loan.getloan("home", 3200, 5);
homeLoan.calculateInterest();

var studentLoan = loan.getloan("student", 1800, 4);
studentLoan.calculateInterest();

var personalLoan = loan.getloan("personal", 1200, 2);
personalLoan.calculateInterest();
```

## Sample Output

```javascript
1280;
216;
120;
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
//implement other functions here
function Loans() {
  //implement Loan function here
}
```
