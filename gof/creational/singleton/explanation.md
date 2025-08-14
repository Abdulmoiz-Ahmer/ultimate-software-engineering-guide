# What is the Singleton Pattern?

The singleton pattern is a type of creational pattern that restricts the instantiation of a class to a single object. This allows the class to create an instance of the class the first time it is instantiated. However, on the next try, the existing instance of the class is returned. No new instance is created.

## Example

A real-life example is a printer a couple of office employees want to use. It'll be a shared resource amongst all the employees. Hence, a single instance of the printer is required so that everyone can share instead of having a new instance for each employee who wants to print something.

```Javascript
let instance = null;
class Printer {
  constructor(pages) {
    this.display = function(){
      console.log(`You are connected to the printer. You want to print ${pages} pages.`)
    }
  }

  static getInstance(numOfpages){
    if(!instance){
      instance = new Printer(numOfpages);
    }
    return instance;
  }
}

var obj1 = Printer.getInstance(2)
console.log(obj1)
obj1.display()
var obj2 = Printer.getInstance(3)
console.log(obj2)
obj2.display()
console.log(obj2 == obj1)
```

## Explanation

In the example above, we are implementing the singleton pattern. The class Printer can only have a single instance. We ensure this in the getInstance function. Let's look at it in detail.

The getInstance function accepts the parameter numOfpages. Inside the function, in line 10, we check if an instance for the Printer class already exists.

```Javascript
if(!instance) //line 10
```

If it does not exist, the code inside the if condition executes and a new instance is created.

```Javascript
instance = new Printer(numOfpages)
```

However, if an instance already exists, it simply returns the existing instance instead of creating a new one.

```Javascript
return instance
```

You can see this in the output as well. We create an instance of the Printer with 2 passed as the argument to getInstance:

```Javascript
var obj1 = Printer.getInstance(2)
console.log(obj1) //line 18
obj1.display() //line 19
```

For lines 18 & 19, you see the following output on the console:

```Javascript
"Printer { display: [Function] }"
"You are connected to the printer. You want to print 2 pages."
```

Next, we try to create a second instance of the Printer with 3 passed as the argument to getInstance.

```Javascript
var obj2 = Printer.getInstance(3)
console.log(obj2) //line 21
obj2.display() //line 22
```

You can see the following output for the commands on lines 21 & 22:

```Javascript
"Printer { display: [Function] }"
"You are connected to the printer. You want to print 2 pages."
```

As you can see, instead of a new instance, the same instance is returned. Hence, obj2.display shows 2 pages instead of 3 pages. Line 23 also returns true, showing that both the instances are the same.

```Javascript
console.log(obj2 == obj1) //line 23
```

## When to Use the Singleton Pattern

The singleton pattern is primarily used in scenarios where you need a single object to coordinate actions across a system. Common use cases include:

### Services

- Services often work best as singletons since they:
  - Store application state
  - Maintain configuration settings
  - Provide access to shared resources
- Having a single service instance ensures consistent access across an application

### Database Connections

- Database systems like MongoDB use the singleton pattern for:
  - Connection pooling
  - Managing database sessions
  - Maintaining a single point of access to the database

### Configuration Objects

- When working with configuration settings that should:
  - Remain consistent throughout the application
  - Avoid unnecessary duplication
  - Provide centralized access to settings
