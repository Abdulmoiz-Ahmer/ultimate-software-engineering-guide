## What is the Factory Pattern?

The **Factory Pattern** is a _creational pattern_ that provides a template for creating objects.  
It is particularly useful in complex situations where the type of object required varies and must be specified in each case.

Unlike directly using the `new` keyword to instantiate objects, the factory pattern avoids explicit constructor calls.  
Instead, it provides a **generic interface** that delegates the object creation responsibility to the corresponding subclass.

---

### Example

As the name _factory_ implies, we can use this pattern when we want to create different objects that share similar characteristics.

```Javascript
class IceCreamFactory {
  constructor() {
    this.createIcecream = function (flavor) {
      let iceCream;
      if (flavor === "chocolate") {
        iceCream = new Chocolate();
      } else if (flavor === "mint") {
        iceCream = new Mint();
      } else if (flavor === "strawberry") {
        iceCream = new Strawberry();
      }
      return iceCream;
    };
  }
}

class Chocolate {
  constructor() {
    this.icecreamFlavor = "chocolate";
    this.message = function () {
      return `You chose the ${this.icecreamFlavor} flavor.`;
    };
  }
}

class Mint {
  constructor() {
    this.icecreamFlavor = "mint";
    this.message = function () {
      return `You chose the ${this.icecreamFlavor} flavor.`;
    };
  }
}

class Strawberry {
  constructor() {
    this.icecreamFlavor = "strawberry";
    this.message = function () {
      return `You chose the ${this.icecreamFlavor} flavor.`;
    };
  }
}

// Creating objects
const iceCreamfactory = new IceCreamFactory();

const chocolate = iceCreamfactory.createIcecream("chocolate");
const mint = iceCreamfactory.createIcecream("mint");
const strawberry = iceCreamfactory.createIcecream("strawberry");

console.log(chocolate.message());
console.log(mint.message());
console.log(strawberry.message());
```

### Explanation

In the example above, we created a factory called `IceCreamFactory`.  
Its constructor contains the method `createIcecream` which accepts a `flavor` parameter.

Depending on the flavor, it instantiates an object of the corresponding class.

For example, if the flavor is `"chocolate"`, it creates a `Chocolate` object.  
The same process applies for `"mint"` and `"strawberry"` flavors.

This approach allows us to centralize and streamline the object creation process.

---

### When to Use the Factory Pattern?

- When the type of objects required cannot be determined beforehand.
- When multiple objects share similar characteristics.
- When you want to generalize the object instantiation process, especially when the setup is complex.
