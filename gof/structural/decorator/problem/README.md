# Challenge: Decorator Pattern

In this challenge, you have to implement the **Decorator Pattern** to solve the given problem.

---

## Problem Statement

The code below implements functionality to **customize superheroes** for a game.

- Every superhero has a **base power**.
- In addition, you can create superheroes with:
  - A **sword**
  - **Super speed**
  - Or **both sword and super speed**

---

## Instructions

Run the code below to see its implementation:

```javascript
class SuperHero {
  constructor(name, power) {
    this.name = name;
    this.power = power;
  }
}

class SuperHeroWithSword extends SuperHero {
  constructor(name, power) {
    super(name, power);
    this.sword = true;
  }
  hasSword() {
    return `${this.name}'s power is ${this.power}, and he also has a sword now.`;
  }
}

class SuperHeroWithSuperSpeed extends SuperHero {
  constructor(name, power) {
    super(name, power);
    this.superSpeed = true;
  }
  hasSuperSpeed() {
    return `${this.name}'s power is ${this.power}, and he also has the super speed now.`;
  }
}

class SuperHeroWithSpeedandSword extends SuperHero {
  constructor(name, power) {
    super(name, power);
    this.speedAndSword = true;
  }
  hasSpeedAndSword() {
    return `${this.name}'s power is ${this.power}, and he also has both super speed and a sword now.`;
  }
}

var superhero1 = new SuperHeroWithSword("Fire Man", "Fire");
console.log(superhero1.hasSword());

var superhero2 = new SuperHeroWithSuperSpeed("Fire Man", "Fire");
console.log(superhero2.hasSuperSpeed());

var superhero3 = new SuperHeroWithSpeedandSword("Ice Man", "Ice");
console.log(superhero3.hasSpeedAndSword());
```

## Task: Extend the Decorator Pattern

If you carefully study the code, you’ll notice that a superhero can currently have **only one** of the three available customizations.

---

### Your Task

Modify the code so that a single superhero object can have **multiple customizations** applied at the same time.

---

### Input

A **multiclass version** of the code for creating superheroes with different superpowers.

---

### Output

Messages displaying **multiple superpowers** of a superhero.

### Sample input

```javascript
var superhero1 = new SuperHero("Fire Man", "Fire");
SuperHeroWithSword(superhero1);
SuperHeroWithSuperSpeed(superhero1);
var superhero2 = new SuperHero("Ice Man", "Ice");
SuperHeroWithSpeedandSword(superhero2);
```

### Sample output

```javascript
`Fire Man's power is Fire, and he also has a sword now.``Fire Man's power is Fire, and he also has the super speed now.``Ice Man's power is Ice, and he also has both super speed and a sword now.`;
```

### Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class SuperHero {
  constructor(name, power) {
    this.name = name;
    this.power = power;
  }
}

class SuperHeroWithSword extends SuperHero {
  constructor(name, power) {
    super(name, power);
    this.sword = true;
  }
  hasSword() {
    return `${this.name}'s power is ${this.power}, and he also has a sword now.`;
  }
}

class SuperHeroWithSuperSpeed extends SuperHero {
  constructor(name, power) {
    super(name, power);
    this.superSpeed = true;
  }
  hasSuperSpeed() {
    return `${this.name}'s power is ${this.power}, and he also has the super speed now.`;
  }
}

class SuperHeroWithSpeedandSword extends SuperHero {
  constructor(name, power) {
    super(name, power);
    this.speedAndSword = true;
  }
  hasSpeedAndSword() {
    return `${this.name}'s power is ${this.power}, and he also has both super speed and a sword now.`;
  }
}
```
