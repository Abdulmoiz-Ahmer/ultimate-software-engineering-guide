# Challenge: Flyweight Pattern

In this challenge, you have to implement the flyweight pattern to solve the given problem.

---

## Problem Statement

In this challenge, you have been given the **Dress** class.

First, you need to define the **dressPrice** function, which is used to set the **price** of a dress and return it. The prices of different **type** of dresses are as follows:

- **maxi**: **1000**
- **gown**: **2000**
- **skirt**: **500**

Every dress has a unique **serialNumber** and there cannot be multiple dresses with the same **serialNumber**. However, in the code given below, there is no such restriction. It allows dresses with the same **serialNumber** to be created more than once:

```javascript
class Dress {
  constructor(serialNumber, type, color, designer, availability) {
    this.serialNumber = serialNumber;
    this.type = type;
    this.color = color;
    this.designer = designer;
    this.availability = availability;
    this.price = 0;
  }
  dressPrice() {
    //define
  }
}

const pinkdress1 = new Dress("#123", "skirt", "pink", "Zara", "yes");
const pinkdress2 = new Dress("#123", "skirt", "pink", "Zara", "yes");
console.log(pinkdress1 === pinkdress2);
```

As you can see, line 17 returns **false**, meaning two dresses with the same **serialNumber** exist. You need to implement the flyweight pattern such that the condition:

```javascript
console.log(pinkdress1 === pinkdress2);
```

evaluates to **true**. Here is how you can achieve this:

Implement a **DressFactory** class which has a **createDress** function. The function definition should not allow different instances of the same **serialNumber** dress to be created.

### Input

Two dresses with the same **serialNumber** created and **dressPrice** function called on them

---

### Output

Both instances should be the same and the **price** for both should be returned

### Sample input

```javascript
const factory = new DressFactory();
const pinkdress1 = factory.createDress("#123", "skirt", "pink", "Zara", "yes");
const pinkdress2 = factory.createDress("#123", "skirt", "pink", "Zara", "yes");

console.log(pinkdress1 === pinkdress2);
console.log(pinkdress1.dressPrice());
console.log(pinkdress2.dressPrice());
```

### Sample output

```javascript
true;
500;
500;
```

### Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class Dress {
  constructor(serialNumber, type, color, designer, availability) {
    this.serialNumber = serialNumber;
    this.type = type;
    this.color = color;
    this.designer = designer;
    this.availability = availability;
    this.price = 0;
  }
  dressPrice() {
    //define
  }
}
```

Let’s discuss the solution in the next lesson.
