# What is the Chain of Responsibility Pattern?

The Chain of Responsibility pattern is a behavioral design pattern that lets you pass a request along a chain of potential handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain. This avoids coupling the sender of a request to its receiver.

A great real-world analogy is **DOM** event bubbling. When you click on a button inside a div, the click event is first sent to the button. If the button doesn't handle it (or after it handles it), the event **"bubbles up"** to the parent div, and so on, up to the root of the document. Each element in the hierarchy gets a chance to handle the event.

## A Practical Example: Number Divisibility Check

Let's implement this pattern to check if a positive integer is a multiple of two, three, or five. We'll create a chain of handlers where each handler is responsible for checking for a specific multiple. If a number is given, it will be passed along the chain until one of the handlers can process it.

We will have three specific handlers:

MultipleofTwoHandler: Checks if the number is a multiple of two.

MultipleofThreeHandler: Checks if the number is a multiple of three.

MultipleofFiveHandler: Checks if the number is a multiple of five.

## The Base Handler

First, we need an abstract base class that all our handlers will inherit from. This class defines the common interface for all handlers: a method to set the next handler and a method to process the request.

```javascript
// Base class for all handlers
class HandlerChain {
  constructor() {
    this.nextObjInChain = null;
  }

  setNextObj(nextObj) {
    this.nextObjInChain = nextObj;
  }

  // Default behavior: if no specific handler processes it, this will run.
  processMultiple(req) {
    console.log("No handler for: " + req.getMultiple());
  }
}
```

The **setNextObj** method is used to link handlers together, and the **processMultiple** method contains the default logic if a request makes it to the end of the chain without being handled.

## The Request Object

The request itself will be encapsulated in a simple object. This object holds the data that needs to be processed.

```javascript
// The request object, containing the number to be checked
class Multiple {
  constructor(number) {
    this.multiple = number;
  }

  getMultiple() {
    return this.multiple;
  }
}
```

## The Concrete Handlers

Now, let's create our specific handlers. Each one will extend HandlerChain and implement its own **processMultiple** logic. If a handler cannot process the request, it must pass it to the next object in the chain.

Here is the implementation for **MultipleofTwoHandler**. The other handlers for three and five follow the exact same structure, just changing the divisor.

```javaScript
class MultipleofTwoHandler extends HandlerChain {
processMultiple(req) {
if (req.getMultiple() % 2 === 0) {
console.log("Multiple of 2: " + req.getMultiple());
} else if (this.nextObjInChain) {
// Pass to the next handler if it exists
this.nextObjInChain.processMultiple(req);
} else {
// Call the base implementation if it's the end of the chain
super.processMultiple(req);
}
}
}

class MultipleofThreeHandler extends HandlerChain {
processMultiple(req) {
if (req.getMultiple() % 3 === 0) {
console.log("Multiple of 3: " + req.getMultiple());
} else if (this.nextObjInChain) {
this.nextObjInChain.processMultiple(req);
} else {
super.processMultiple(req);
}
}
}

class MultipleofFiveHandler extends HandlerChain {
processMultiple(req) {
if (req.getMultiple() % 5 === 0) {
console.log("Multiple of 5: " + req.getMultiple());
} else if (this.nextObjInChain) {
this.nextObjInChain.processMultiple(req);
} else {
super.processMultiple(req);
}
}
}
```

## Creating and Using the Chain

With our components ready, we can now build the chain and process requests. We instantiate each handler and then link them together using the setNextObj method.

```javascript
// 1. Create handler instances
var c1 = new MultipleofTwoHandler();
var c2 = new MultipleofThreeHandler();
var c3 = new MultipleofFiveHandler();

// 2. Build the chain: c1 -> c2 -> c3
c1.setNextObj(c2);
c2.setNextObj(c3);

// 3. Send requests to the first handler in the chain
console.log("Sending request for 95...");
c1.processMultiple(new Multiple(95)); // Output: Multiple of 5: 95

console.log("\nSending request for 6...");
c1.processMultiple(new Multiple(6)); // Output: Multiple of 2: 6

console.log("\nSending request for 21...");
c1.processMultiple(new Multiple(21)); // Output: Multiple of 3: 21

console.log("\nSending request for 11...");
c1.processMultiple(new Multiple(11)); // Output: No handler for: 11
```

Let's trace the request for the number 95:

The request is sent to c1 (MultipleofTwoHandler).

c1 checks 95 % 2. The condition is false.

c1 passes the request to the next object in its chain, which is c2 (MultipleofThreeHandler).

c2 checks 95 % 3. The condition is false.

c2 passes the request to the next object, c3 (MultipleofFiveHandler).

c3 checks 95 % 5. The condition is true. It handles the request by printing "Multiple of 5: 95" and the chain stops. ✅

## When to Use the Chain of Responsibility Pattern? 🤔

You should consider using this pattern when:

More than one object can handle a request, and you don't know which object will handle it beforehand. The handler is determined at runtime.

You want to send a request to one of several objects without specifying the receiver explicitly.

The set of objects that can handle a request needs to be specified dynamically. You can add or remove handlers from the chain at any time.
