# What is the decorator pattern?

The decorator pattern focuses on adding properties, functionalities, and behavior to existing classes dynamically. The additional decoration functionalities aren’t considered essential enough to be a part of the original class definition as they can cause clutter. Hence, the decorator pattern lets you modify the code without changing the original class.

Unlike the creational patterns, the decorator pattern is a structural pattern that does not focus on object creation rather decoration. Hence, it doesn’t rely on prototypal inheritance alone; it takes the object and keeps adding decoration to it. This makes the process more streamlined. Let’s take a look at an example to understand this concept better.

```javascript
class FrozenYoghurt {
  constructor(flavor, price) {
    this.flavor = flavor;
    this.price = price;
  }

  orderPlaced() {
    console.log(
      `The ${this.flavor} flavor will cost you ${this.price} dollars`
    );
  }
}

// decorator 1
function addFlavors(froyo) {
  froyo.addStrawberry = true;
  froyo.addVanilla = true;
  froyo.price += 20;
  froyo.updatedInfo = function () {
    console.log(
      `The updated price after adding flavors is ${froyo.price} dollars`
    );
  };
  return froyo;
}

// decorator 2
function addToppings(froyo) {
  froyo.hasSprinkles = true;
  froyo.hasBrownie = true;
  froyo.hasWafers = true;
  froyo.allToppings = function () {
    console.log("Your froyo has sprinkles, brownie, and wafers");
  };
  return froyo;
}

//using decorators
//creating a froyo
const froyo = new FrozenYoghurt("chocolate", 10);
froyo.orderPlaced();
//adding flavors
var froyowithFlavors = addFlavors(froyo);
froyowithFlavors.updatedInfo();
//adding toppings
var froyoWithToppings = addToppings(froyo);
froyoWithToppings.allToppings();
```

1. **Base Step**  
   First, you buy a chocolate froyo. This costs **$10**.

   > This represents the **core object**.

2. **Adding Flavors (Optional)**  
   After getting the base froyo, you have the option to add extra flavors.

   - Some people might just stick with chocolate and leave.
   - In our case, we add **strawberry** and **vanilla**. Each costs **$10**, so the total increases by $20.
     > These extra flavors act like **decorators** that wrap around the base froyo.

3. **Adding Toppings (Optional)**  
   At this point, you can either pay and leave or add toppings.
   - We add **sprinkles**, a **brownie**, and **wafers**.
     > These are also **decorators** — additional layers that enhance the object.

---

We start by creating a FrozenYoghurt class like so:

```javascript
class FrozenYoghurt {
  constructor(flavor, price) {
    this.flavor = flavor;
    this.price = price;
  }

  orderPlaced() {
    console.log(
      `The ${this.flavor} flavor will cost you ${this.price} dollars`
    );
  }
}
```

Its constructor initializes the flavor and price properties to the values passed into the constructor. It also contains the orderPlaced function, which displays the flavor you got and its price.

Now, it’s time for the decoration. You have the option to addFlavors and addToppings to your froyo.

Here’s what the addFlavors function looks like:

```javascript
function addFlavors(froyo) {
  froyo.addStrawberry = true;
  froyo.addVanilla = true;
  froyo.price += 20;
  froyo.updatedInfo = function () {
    console.log(
      `The updated price after adding flavors is ${froyo.price} dollars`
    );
  };
  return froyo;
}
```

It adds the strawberry and vanilla flavors to the froyo instance and increases the price by 20 dollars. The updatedInfo function shows the updated price.

The addToppings function is as follows:

```javascript
function addToppings(froyo) {
  froyo.hasSprinkles = true;
  froyo.hasBrownie = true;
  froyo.hasWafers = true;
  froyo.allToppings = function () {
    console.log("Your froyo has sprinkles, brownie, and wafers");
  };
  return froyo;
}
```

It adds sprinkles, a brownie, and wafers to the froyo instance. The allToppings function displays all the toppings added.

# When to use the decorator pattern?

JavaScript developers can use the decorator pattern when they want to easily modify or extend the functionality of an object without changing its base code.

It can also be used if an application has a lot of distinct objects with the same underlying code. Instead of creating all of them using different subclasses, additional functionalities can be added to the objects using the decorator pattern.

A simple example is text formatting, where you need to apply different formattings such as bold, italics, and underline to the same text.

Now that you know what a decorator pattern is, it’s time to implement it!
