# Challenge: Facade Pattern

In this challenge, you have to implement the facade pattern to solve the given problem.

---

## Problem Statement

In this challenge, you have to implement a part of an online hair product ordering system. The available products are shampoo, conditioner, and hair serum. A customer who is shopping online can buy any of these. A product object has the following properties:

- productName: name of the product, that is, shampoo, conditioner, or hair serum

- amount: the number of bottles that the customer wants to buy

This system will allow a customer to buy an amount of product. If that amount is available in the inventory, a BuyProduct class instance should be initiated. If the amount is not available, a PreOrderProduct class instance should be initiated. The inventory will look like:

- the amount of shampoo is: 20
- the amount of conditioner is: 20
- the amount of hair serum is: 1000
  In the end, the customers should get a message that lets them know if they can buy that amount of bottles or will have to pre-order. Here’s an example:

---

Run the code below to see its implementation:

```javascript
`2 bottles of shampoo are available. Click on "buy" to purchase them.``2000 bottles of hair serum are not available. You can Pre-order them on the next page.`;
```

### Your Task

You need to implement the facade pattern to achieve this. You’ve already been given the Inventory, BuyingProduct, BuyProduct, and PreOrder classes. Write their definitions and link them such that the output mentioned above is shown to the customer.

---

### Input

buyProduct method invoked with some given arguments

---

### Output

The message displayed regarding whether the customer can buy the products or will have to pre-order them

### Sample input

```javascript
var customer = new BuyingProduct();
customer.buyProduct({ productName: "shampoo", amount: 2 });
customer.buyProduct({ productName: "hair serum", amount: 2000 });
```

### Sample output

```javascript
`2 bottles of shampoo are available. Click on "buy" to purchase them.``2000 bottles of hair serum are not available. You can Pre-order them on the next page.`;
```

### Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class Inventory {
  //initialize the amounts of shampoo, conditioner, and hair serums
  //check availability of products
  //hint: define a function that checks availability
  constructor() {
    this.shampoo = 20;
    this.conditioner = 20;
    this.hairSerum = 1000;
  }

  checkAvailability(product) {
    if (product.productName === "shampoo" && this.shampoo < product.amount) {
      return false;
    } else if (
      product.productName === "conditioner" &&
      this.conditioner < product.amount
    ) {
      return false;
    } else if (
      product.productName === "hair serum" &&
      this.hairSerum < product.amount
    ) {
      return false;
    }
    return true;
  }
}

class BuyingProduct extends Inventory {
  buyProduct(product) {
    if (!this.checkAvailability(product)) {
      return new PreOrderProduct().print(product);
    }

    return new BuyProduct().print(product);
  }
}

class BuyProduct {
  //define it such that it returns a message
  print(product) {
    console.log(
      `${product.amount} bottles of ${product.productName} are available. Click on "buy" to purchase them.`
    );
  }
}

class PreOrderProduct {
  //define it such that it returns a message
  print(product) {
    console.log(
      `${product.amount} bottles of ${product.productName} are not available. You can Pre-order them on the next page.`
    );
  }
}
```
