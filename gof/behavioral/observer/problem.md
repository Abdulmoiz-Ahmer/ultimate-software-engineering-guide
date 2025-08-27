# Challenge: Observer Pattern

## Problem Statement

In this challenge, you have to implement an auction system using the observer pattern.

You have two classes **Auctioneer** (the person conducting the bid) and **Bidder** (the bidder bidding for the object).

Here’s what the **Auctioneer** class needs to do:

- It should maintain a list of all bidders.

- It should have a function **registerBidder** to register the bidders.

- It should have an **announceNewBidderPrice** function to announce the bidding price given by a bidder.

- It should have a **notifyBidders** function to notify each bidder of a new bidding price.

**Bidder** should have the following:

- A **name** and **bidPrice**

- An **update** function that displays the **name** of the bidder along with the **bidPrice** they are giving. For example, **{insert name} is offering {insert bid price} dollars**. It should display **Sold to {insert name of bidder here}** if the bid price exceeds **500** dollars.

- A **giveNewPrice** function that sets the bid price of a bidder

---

## Input

The **announceNewBidderPrice** function is called after different bidders have given their prices

---

## Output

The name of the bidders and the prices they gave are displayed along with the name of the bidder who wins the bid

---

## Sample Input

```javascript
auctioneer = new Auctioneer();
bidder1 = new Bidder("Ross");
auctioneer.registerBidder(bidder1);
bidder2 = new Bidder("Joey");
auctioneer.registerBidder(bidder2);
bidder1.giveNewPrice(400);
bidder2.giveNewPrice(550);
auctioneer.announceNewBidderPrice();
```

## Sample Output

```javascript
"Ross is offering 400 dollars";
"Joey is offering 550 dollars";
"Sold to Joey";
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class Auctioneer {
  constructor() {
    //define constructor here
  }
  //write code here
}

class Bidder {
  constructor() {
    //define constructor here
  }
  //write code here
}
```
