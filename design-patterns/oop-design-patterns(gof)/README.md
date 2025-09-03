# What Are Design Patterns?

## Definition

As developers, we want to write code that is efficient, reusable, and maintainable. Similarly, as JavaScript developers, you can end up writing code for large applications. Hence, the code structure becomes important. While developing, you may also find yourself writing similar code for separate problems. In such scenarios, it’ll be helpful to have a structure that could be used to solve various common issues. This is where **design patterns** come into play.

Design patterns are solutions to commonly occurring problems in software design, such as writing JavaScript web applications. They can also be considered as **templates** that can be used to solve various issues in different situations.

---

## Advantages

Let’s look at some of the advantages of using design patterns:

- **Proven solutions**: They have been derived and optimized by various experienced programmers over time, ensuring that the solutions are correct and efficient.
- **Generic templates**: They can be modified and reused for solving different problems.
- **Clean and elegant code**: They provide a structured way to solve large problems while avoiding repetition in code.
- **Faster development**: Developers can spend less time on code structure and more on improving the overall quality of the solution.
- **Reduced codebase size**: Optimal solutions mean less redundant code.

---

## Drawbacks

While there are many advantages of using design patterns, it is also important to be aware of their drawbacks:

- **Overcomplication**: If managed poorly, they can make the application’s architecture unnecessarily complex.
- **Steep learning curve**: Developers unfamiliar with certain patterns might find it confusing to understand why they are being used.

---

## Types of Design Patterns

Now, we’ll look at some popular design patterns in JavaScript. These include the following:

---

## Creational Design Patterns

These patterns are used to provide a mechanism for creating objects in a specific situation **without revealing the creation method**.  
The normal approach for creating an object might lead to complexities in the design of a project.  
These patterns allow flexibility in deciding which objects need to be created for a specific use case by providing **control over the creation process**.

- [creational](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational)

  - [explanation](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/blob/main/gof/creational/README.md)

  - [factory](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/factory)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/factory/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/factory/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/factory/problem/solution.js)

  - [constructor](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/constructor)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/constructor/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/constructor/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/constructor/problem/solution.js)

  - [singleton](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/singleton)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/singleton/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/singleton/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/singleton/problem/solution.js)

  - [builder](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/builder)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/builder/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/builder/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/builder/problem/solution.js)

  - [prototype](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/prototype)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/prototype/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/prototype/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/prototype/problem/solution.js)

  - [abstract](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/abstract)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/abstract/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/abstract/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/abstract/problem/solution.js)

---

## Structural Design Patterns

These patterns focus on **class/object composition** and the relationships between objects.  
They allow you to add new functionalities to objects so that **restructuring some parts of the system does not affect the rest**.  
Hence, when some parts of the structure change, the entire system does not need to be modified.

- [structural](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural)

  - [explanation](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/blob/main/gof/structural/README.md)

  - [decorator](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/decorator)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/decorator/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/decorator/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/decorator/problem/solution.js)

  - [facade](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/facade)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/facade/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/facade/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/facade/problem/solution.js)

  - [adapter](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/adapter)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/adapter/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/adapter/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/adapter/problem/solution.js)

  - [bridge](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/bridge)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/bridge/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/bridge/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/bridge/problem/solution.js)

  - [composite](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/composite)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/composite/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/composite/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/composite/problem/solution.js)

  - [flyweight](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/flyweight)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/flyweight/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/flyweight/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/flyweight/problem/solution.js)

  - [proxy](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/proxy)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/proxy/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/proxy/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/proxy/problem/solution.js)

---

## Behavioral Design Patterns

These patterns are concerned with **communication between dissimilar objects** in a system.  
They streamline communication and ensure that **information is synchronized** between such objects.

- [behavioral](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral)

  - [explanation](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/blob/main/gof/behavioral/README.md)

  - [chain-of-responsibility](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/chain-of-responsibility)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/chain-of-responsibility/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/chain-of-responsibility/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/chain-of-responsibility/problem/solution.js)

  - [command](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/command)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/command/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/command/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/command/problem/solution.js)

  - [iterator](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/iterator)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/iterator/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/iterator/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/iterator/problem/solution.js)

  - [mediator](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/mediator)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/mediator/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/mediator/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/mediator/problem/solution.js)

  - [observer](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/observer)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/observer/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/observer/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/observer/problem/solution.js)

  - [visitor](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/visitor)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/visitor/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/visitor/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/visitor/problem/solution.js)

---

## Architectural Design Patterns

These patterns are used for **solving architectural problems** within a given context in software architecture.

- [architectural](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural)

  - [explanation](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/blob/main/gof/architectural/README.md)

  - [mvc](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvc)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvc/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvc/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvc/problem/solution.js)

  - [mvp](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvp)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvp/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvp/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvp/problem/solution.js)

  - [mvvm](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvvm)

    - [README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvvm/README.md)
    - [problem/README.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvvm/problem/README.md)
    - [problem/solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvvm/problem/solution.js)
