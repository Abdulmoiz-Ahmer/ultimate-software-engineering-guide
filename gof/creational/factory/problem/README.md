## Challenge: Factory Pattern

### Problem Statement

You need to implement a factory `ToyFactory` that can create a toy duck or a toy car object using either the `ToyDuck` or `ToyCar` function constructor.

A **ToyDuck** object should have the following properties:

- `color`
- `price`

A **ToyCar** object should have the following properties:

- `color`
- `price`
- `name`

As you can see in **line 2**, by default, the toy is of `ToyDuck` class:

```js
this.toy = ToyDuck;
```

Your task is to create a function `createToy`.  
It should decide which toy to create depending on the parameter passed to it.

---

**Input**

- `createToy` function called with different parameters.

**Output**

- Toy **duck** or **car** object created depending on the inputs.

Sample input

```js
var toyFactory = new ToyFactory();
var car = toyFactory.createToy({
  toyType: "car",
  color: "blue",
  price: 12,
  name: "honda",
});
```

Sample output

```js
ToyCar { color: 'blue', price: 12, name: 'honda' }
```

Challenge
Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```js
function ToyFactory() {
  this.toy = ToyDuck; //toy property set to ToyDuck by default
}

function ToyDuck() {} //define the ToyDuck class

function ToyCar() {} //define the ToyCar class
```
