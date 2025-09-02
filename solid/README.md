# A Deep Dive into SOLID Principles

The **SOLID** principles are a set of five essential design principles in object-oriented programming that guide developers in creating software that is more understandable, flexible, and maintainable. When applied correctly, these principles help manage complexity, reduce coupling, and improve the scalability of your code.

SOLID is an acronym representing the following five principles:

- **S** - Single Responsibility Principle (SRP)

- **O** - Open/Closed Principle (OCP)

- **L** - Liskov Substitution Principle (LSP)

- **I** - Interface Segregation Principle (ISP)

- **D** - Dependency Inversion Principle (DIP)

Let's explore each principle with practical ```Javascript examples.

## Single Responsibility Principle (SRP)

A class should have only one reason to change, meaning it should have only one responsibility.

This principle encourages creating small, focused classes. A class should not be a "Swiss Army knife" handling unrelated tasks like user management, database operations, and email notifications all at once.

**Without SRP**
In this example, the User class is responsible for managing the user's name, saving the user to a database, and sending emails. It has multiple reasons to change.

```Javascript

class User {
constructor(name) {
this.name = name;
}

getName() {
return this.name;
}

saveToDatabase() {
// Code for saving the user to the database
console.log(`Saving ${this.name} to the database.`);
}

sendEmail() {
// Code for sending an email to the user
console.log(`Sending email to ${this.name}.`);
}
}
```

**With SRP**
By applying SRP, we separate these concerns into distinct classes. Each class now has a single responsibility.

```Javascript

// Handles user data
class User {
constructor(name) {
this.name = name;
}

getName() {
return this.name;
}
}

// Handles database interactions for the user
class UserRepository {
saveToDatabase(user) {
// Code for saving the user to the database
console.log(`Saving ${user.getName()} to the database.`);
}
}

// Handles sending emails
class EmailService {
sendEmail(user) {
// Code for sending an email to the user
console.log(`Sending email to ${user.getName()}.`);
}
}
```

**Takeaway**: This separation makes the system easier to maintain. If you need to change the database logic, you only modify UserRepository without touching User or EmailService.

## Open/Closed Principle (OCP)

Software entities (classes, modules, functions) should be open for extension but closed for modification.

This means you should be able to add new functionality without altering existing, tested code. This is often achieved through inheritance or strategy patterns.

### Example 1: Calculating Area of Shapes\*\*

**Without OCP**
If we need to calculate the area for different shapes, a common approach is to check the type of the shape and perform the calculation. Adding a new shape (e.g., Triangle) would require modifying the AreaCalculator function.

```Javascript

class Rectangle {
constructor(width, height) {
this.width = width;
this.height = height;
}
}

class Circle {
constructor(radius) {
this.radius = radius;
}
}

// This function must be modified for every new shape
function calculateTotalArea(shapes) {
let totalArea = 0;
for (const shape of shapes) {
if (shape instanceof Rectangle) {
totalArea += shape.width _ shape.height;
}
if (shape instanceof Circle) {
totalArea += Math.PI _ shape.radius \* shape.radius;
}
// Add another 'if' for Triangle, Square, etc.
}
return totalArea;
}
```

**With OCP**
A better approach is to create a base Shape class with a calculateArea method. Each specific shape extends this class and provides its own implementation. The system is now open to adding new shapes without changing any existing code.

```Javascript

class Shape {
calculateArea() {
throw new Error("Subclasses must implement the 'calculateArea' method.");
}
}

class Rectangle extends Shape {
constructor(width, height) {
super();
this.width = width;
this.height = height;
}

calculateArea() {
return this.width \* this.height;
}
}

class Circle extends Shape {
constructor(radius) {
super();
this.radius = radius;
}

calculateArea() {
return Math.PI _ this.radius _ this.radius;
}
}

// This function no longer needs modification
function calculateTotalArea(shapes) {
return shapes.reduce((sum, shape) => sum + shape.calculateArea(), 0);
}
```

### Example 2: Shopping Cart Discount Strategy

Here, the ShoppingCart can apply different discount strategies. We can add new discount types without modifying the ShoppingCart class itself.

```Javascript

// Base strategy - open for extension
class DiscountStrategy {
applyDiscount(price) {
throw new Error("Subclasses must implement the 'applyDiscount' method.");
}
}

// Concrete strategy - closed for modification
class PercentageDiscount extends DiscountStrategy {
constructor(percentage) {
super();
this.percentage = percentage;
}

applyDiscount(price) {
return price - (price \* (this.percentage / 100));
}
}

// Another concrete strategy - closed for modification
class FixedAmountDiscount extends DiscountStrategy {
constructor(discountAmount) {
super();
this.discountAmount = discountAmount;
}

applyDiscount(price) {
return price - this.discountAmount;
}
}

// The context class is closed for modification
class ShoppingCart {
constructor() {
this.items = [];
}

addItem(item) {
this.items.push(item);
}

calculateTotal(discountStrategy) {
const total = this.items.reduce((acc, item) => acc + item.price, 0);
return discountStrategy.applyDiscount(total);
}
}
```

## Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types without altering the correctness of the program.

This means that if a class S is a subtype of class T, an object of type T should be replaceable with an object of type S without breaking the program.

**Violating LSP**
The classic example involves birds. If we have a Bird base class with a fly method, an Ostrich subtype would violate LSP because an ostrich cannot fly. Replacing a Bird object with an Ostrich object would lead to unexpected behavior or errors.

```Javascript

class Bird {
fly() {
console.log("This bird is flying");
}
}

class Ostrich extends Bird {
// Ostriches cannot fly, so this method is problematic
fly() {
throw new Error("Ostrich cannot fly");
}
}

function makeBirdFly(bird) {
bird.fly();
}

const genericBird = new Bird();
const ostrich = new Ostrich();

makeBirdFly(genericBird); // Works fine
// makeBirdFly(ostrich); // Throws an error, violating LSP
```

**Adhering to LSP**
Let's look at a Stack example. A FixedStack with a capacity limit can still be substituted for a regular Stack as long as it correctly implements the stack's contract (push, pop, etc.), even with its added constraints.

```Javascript

class Stack {
constructor() {
this.items = [];
}

push(item) {
this.items.push(item);
}

pop() {
return this.items.pop();
}

size() {
return this.items.length;
}
}

class FixedStack extends Stack {
constructor(capacity) {
super();
this.capacity = capacity;
}

push(item) {
if (this.size() < this.capacity) {
super.push(item);
} else {
throw new Error("Stack is full");
}
}
}

// A function expecting a base Stack can safely use a FixedStack
function useStack(stack) {
stack.push(1);
stack.push(2);
console.log(stack.size()); // 2
stack.pop();
console.log(stack.size()); // 1
}

const standardStack = new Stack();
const fixedStack = new FixedStack(5);

useStack(standardStack); // Works
useStack(fixedStack); // Also works, adhering to LSP
```

## Interface Segregation Principle (ISP)

Clients should not be forced to depend on interfaces they do not use.

This principle advocates for creating smaller, more specific interfaces rather than large, general-purpose ones. Clients should only need to know about the methods that are relevant to them.

**Without ISP**
Here, we have a "fat" Worker interface. A Manager only needs the work method, but is forced to know about the eat method as well.

```Javascript

class Worker {
work() {
console.log("Working...");
}

eat() {
console.log("Eating...");
}
}

class Manager {
manage(worker) {
worker.work();
}
}
```

**With ISP**
We can segregate the responsibilities into smaller interfaces (or classes in Javascript's context). This way, a client like Manager only depends on the Workable interface.

```Javascript

class Workable {
work() {
console.log("Working...");
}
}

class Eatable {
eat() {
console.log("Eating...");
}
}

class HumanWorker extends Workable, Eatable {
// In JS, you'd use composition or multiple class extensions
}

class RobotWorker extends Workable {
// Robots work but don't eat
}

class Manager {
manage(worker) { // worker must be of type Workable
worker.work();
}
}
```

## Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.

This principle promotes decoupling by ensuring that high-level policy-setting modules are not dependent on low-level implementation details. This is often achieved through Dependency Injection.

**Without DIP**
In this example, the high-level Switch module directly depends on the low-level LightBulb module. If we want the switch to control a Fan, we would have to modify the Switch class.

```Javascript

class LightBulb {
turnOn() {
console.log("LightBulb: ON");
}

turnOff() {
console.log("LightBulb: OFF");
}
}

class Switch {
constructor(bulb) { // Directly depends on LightBulb
this.bulb = bulb;
this.isOn = false;
}

operate() {
this.isOn = !this.isOn;
if (this.isOn) {
this.bulb.turnOn();
} else {
this.bulb.turnOff();
}
}
}
```

**With DIP**
By introducing an abstraction (SwitchableDevice), the Switch class can work with any device that implements this interface. The Switch no longer depends on the concrete LightBulb class.

```Javascript

// Abstraction
class SwitchableDevice {
turnOn() {
throw new Error("This method should be overridden!");
}
turnOff() {
throw new Error("This method should be overridden!");
}
}

// Low-level module depending on abstraction
class LightBulb extends SwitchableDevice {
turnOn() {
console.log("LightBulb: ON");
}
turnOff() {
console.log("LightBulb: OFF");
}
}

// Another low-level module
class Fan extends SwitchableDevice {
turnOn() {
console.log("Fan: ON");
}
turnOff() {
console.log("Fan: OFF");
}
}

// High-level module depending on abstraction
class Switch {
constructor(device) { // Depends on SwitchableDevice abstraction
this.device = device;
this.isOn = false;
}

operate() {
this.isOn = !this.isOn;
if (this.isOn) {
this.device.turnOn();
} else {
this.device.turnOff();
}
}
}

const bulb = new LightBulb();
const fan = new Fan();

const bulbSwitch = new Switch(bulb);
const fanSwitch = new Switch(fan);

bulbSwitch.operate(); // LightBulb: ON
fanSwitch.operate(); // Fan: ON
```

## Conclusion

By adhering to the SOLID principles, you can create systems that are more robust, maintainable, and scalable. These principles encourage better code organization, reduce complexity, and make it easier to introduce new features or fix bugs without breaking existing functionality. While they may require more upfront thought, the long-term benefits in code quality are well worth the effort.
