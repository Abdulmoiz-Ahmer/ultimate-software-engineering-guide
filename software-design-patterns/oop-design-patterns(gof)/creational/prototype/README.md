# What is the Prototype Pattern?

The **prototype creational pattern** is used to instantiate objects with some default values using an existing object. It clones the object and provides the existing properties to the cloned object using **prototypal inheritance**.

In prototypal inheritance, a prototype object acts as a blueprint from which other objects inherit when the constructor instantiates them. Hence, any properties defined on the prototype of a constructor function will also be present in the cloned object it creates.

For example, imagine you have a `car` object that serves as a blueprint. You can use it to create other car objects, such as **car1** and **car2**, which will automatically have the same properties and methods as the original `car`.  
In JavaScript, this can be done using the `Object.create` method.

---

```javascript
var car = {
  drive() {
    console.log("Started Driving");
  },
  brake() {
    console.log("Stopping the car");
  },
  numofWheels: 4,
};

const car1 = Object.create(car);
car1.drive();
car1.brake();
console.log(car1.numofWheels);

const car2 = Object.create(car);
car2.drive();
car2.brake();
console.log(car2.numofWheels);
```

## Explanation

From the code above, you can see that both **car1** and **car2** have the properties and methods present in the **car** object.

What does `Object.create` do?  
`Object.create` takes an object as a parameter (car in our case) and returns an object whose **prototype property** points to this object (car).

```javascript
var car = {
  drive() {
    console.log("Started Driving");
  },
  brake() {
    console.log("Stopping the car");
  },
  numofWheels: 4,
};

const car1 = Object.create(car);
console.log(car1.__proto__ == car);

const car2 = Object.create(car);
console.log(car2.__proto__ == car);
```

As you can see, the prototype property of both **car1** and **car2**, accessed using `__proto__`, is **car**.

You can also define an extra property for the new object using `Object.create`.  
Let’s add additional properties to **car1** and **car2**.

```javascript
var car = {
  drive() {
    console.log("Started Driving");
  },
  brake() {
    console.log("Stopping the car");
  },
  numofWheels: 4,
};

//defining the extra property color with value red
const car1 = Object.create(car, { color: { value: "red" } });
console.log(car1.color);

//defining the extra property color with value red black
const car2 = Object.create(car, { color: { value: "red black" } });
console.log(car2.color);
```

In the example, we added the `color` property to both **car1** and **car2** with their values set to `"red"` and `"red black"` respectively.

---

## When to Use the Prototype Pattern?

The prototype pattern has **native support** in JavaScript. It involves cloning an already-configured object. Hence, the cloned objects are created **by reference** instead of having their own separate copies. This boosts performance and efficiency.

Use this pattern when:

- You want to **eliminate the overhead** of initializing an object.
- You want the system to be **independent of how products are created**.
- You are **creating objects from a database**, whose values are copied to the cloned object.
