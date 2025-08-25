# Challenge: MVC Pattern

In this challenge, you have to implement the **MVC (Model-View-Controller)** pattern to solve the given problem.

---

## Problem Statement

You need to implement the **MVC pattern** to **display the items in a shopping cart**.

There are three main components:

---

## **1. ShoppingCartModel**

The **shopping cart model** should have the following properties:

- `itemNumber`
- `itemName`
- `itemQuantity`
- `itemPrice`

Additionally, it should have a **getter function** for each property.

---

## **2. ShoppingCartView**

You are already given part of the code that:

- Initializes the **current view** for the controller
- Implements the **`displayItem`** function to show an item's details.

### Your tasks:

- **Implement a `buyItem` function** to **buy an item**.
- **Implement a `changeItemQuantity` function** to **update the quantity** of an item in the cart.

#### `changeItemQuantity` Parameters:

- `itemNumber`
- `newQuantity`

---

## **3. ShoppingCartController**

The **controller** should:

- **Update the view** whenever a change occurs in the **shopping cart model**.
- **Reflect changes** in the model if the **user edits the view**.

---

## **Input**

- The `buyItem` function is called to **add items** to the cart.
- The `changeItemQuantity` function is called to **update an existing item's quantity**.

---

## **Output**

- The **items in the cart** are displayed.

---

## **Sample Input**

```javascript
var view = new ShoppingCartView();
var controller = new ShoppingCartController();
view.registerWith(controller);
view.buyItem("Popcorn", 3, 2.5);
view.changeItemQuantity(0, 6);
```

## Sample Output

```javascript
"Item Number: 0";
"Item: Popcorn";
"Quantity: 3";
"Price: 2.5";
"Item Number: 0";
"Item: Popcorn";
"Quantity: 6";
"Price: 2.5";
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class ShoppingCartModel {
  //write code here
}

class ShoppingCartView {
  constructor() {
    this.controller = null;
  }
  registerWith(controller) {
    this.controller = controller;
    this.controller.addView(this);
  }

  displayItem(itemNumber, itemName, itemQuantity, itemPrice) {
    console.log(
      `Item Number: ${itemNumber}\nItem: ${itemName}\nQuantity: ${itemQuantity}\nPrice: ${itemPrice}`
    );
  }

  //write code here
}

class ShoppingCartController {
  constructor() {
    this.model = null;
    this.view = null;
    this.itemList = [];
  }

  addView(view) {
    this.view = view;
  }
  addModel(model) {
    this.model = model;
  }

  //write code here
}
```
