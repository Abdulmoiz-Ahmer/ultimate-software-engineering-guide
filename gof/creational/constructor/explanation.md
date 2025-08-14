# Constructor Pattern in JavaScript

## What is the Constructor Pattern?

As a JavaScript developer, you may have encountered **constructors** at some point. These are special functions that initialize objects with specific properties and methods.

The **constructor pattern**, as the name implies, is a class-based pattern that uses the constructors present in the class to create specific types of objects.

---

## Example

There are many ways to create objects in JavaScript, such as:

- Using the `{}` notation
- Using `Object.create`

However, in JavaScript, the use of the **constructor pattern** is very popular as it can create multiple objects of a specific kind.

### Example Code

```javascript
function Human(name, age, occupation) {
  // ES5 function-based constructor
  // Defining properties inside the constructor function
  this.name = name;
  this.age = age;
  this.occupation = occupation;

  // Defining a method inside the constructor function
  this.describe = function () {
    console.log(`${this.name} is a ${this.age}-year-old ${this.occupation}`);
  };
}

// Creating a "person" object using the Human constructor
var person = new Human("Elle", "23", "Engineer");

// Calling the describe method for the person object
person.describe();
```

### Explanation

In ES5 JavaScript, functions can be used as constructors to instantiate objects.

In the example above, the constructor function Human is defined with:

Properties:

- name
- age
- occupation

Method:

```javascript
describe();
```

When we run:

```javascript
var person = new Human("Elle", "23", "Engineer");
```

A new object is created using the new keyword.

The constructor assigns the provided arguments to the new object’s properties.

The object also gets the describe method.

## When we call:

```javascript
person.describe();
```

It outputs:

```javascript
Elle is a 23-year-old Engineer
```

### How Does this Work Here?

Inside the constructor function:

```javascript
this.name = name;
this.age = age;
this.occupation = occupation;
```

this refers to the new object being created (person in this case).

Similarly, in:

```javascript
console.log(`${this.name} is a ${this.age}-year-old ${this.occupation}`);
```

this still refers to the newly created object, which is why it prints the correct property values.

### Creating Multiple Objects

We can use the same constructor to create multiple objects:

```javascript
function Human(name, age, occupation) {
  this.name = name;
  this.age = age;
  this.occupation = occupation;
  this.describe = function () {
    console.log(`${this.name} is a ${this.age}-year-old ${this.occupation}`);
  };
}

var person = new Human("Elle", "23", "Engineer");
person.describe();

// Creating a second object
var newperson = new Human("Joe", "13", "Painter");
newperson.describe();
```

Output:

```javascript
Elle is a 23-year-old Engineer
Joe is a 13-year-old Painter
```

Here, this refers to the new object being created each time.

### When to Use the Constructor Pattern?

Use this pattern when you want to create multiple instances from the same template, where:

Instances share methods.

Instances can still have different property values.

#### Common use cases:

- Libraries
- Plugins
