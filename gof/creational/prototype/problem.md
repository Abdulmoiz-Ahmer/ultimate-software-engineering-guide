# Challenge: Prototype Pattern

## Problem Statement

You need to implement a **Ninja fighting game** using the prototype pattern.

You have already been given the `Ninja` constructor function, which will be used to create a ninja object.  
A ninja should have the following properties:

- `name`
- `points` (default: 100 upon instantiation)

A ninja can perform the following moves in a fight:

- **punch**: The opponent’s points reduce by **20** if they get punched.
- **kick**: The opponent’s points reduce by **50** if they get kicked.

---

## Rules for Attacks

A ninja can only kick or punch another ninja if:

1. The opponent’s points are **greater than 0**.
2. The attacking ninja’s points are **greater than 0**.

If both conditions are met, you should return the updated points of the opponent.

```javascript
`{other ninja's "name"} points are {other ninja's "points"}`;
```

If the conditions are **not met**:

- For a punch attempt, return:

```javascript
`Can't punch {other ninja's name}`;
```

- For a kick attempt, return:

```javascript
`Can't kick {other ninja's name}`;
```

---

## Input

Two ninjas fighting.

---

## Output

The points of the ninja after being hit **or**
The `"Can’t kick"` / `"Can’t punch"` message.

---

## Sample Input

```javascript
var ninja1 = new Ninja("Ninja1");
var ninja2 = new Ninja("Ninja2");

ninja1.kick(ninja2);
ninja2.punch(ninja1);
ninja1.kick(ninja2);
ninja1.punch(ninja2);
ninja2.kick(ninja1);
```

---

## Sample Output

```
"Ninja2's points are 50"
"Ninja1's points are 80"
"Ninja2's points are 0"
"Can't punch Ninja2"
"Can't kick Ninja1"
```

---

## Challenge

Take a close look at this problem and design a **step-by-step solution** before jumping into the implementation.  
This problem is designed for **your practice**, so try to solve it on your own first.  
If you get stuck, you can always refer to the solution provided.

**Good luck!**

```
//Define the Ninja class and write rest of the code here
const Ninja = function() {}
```
