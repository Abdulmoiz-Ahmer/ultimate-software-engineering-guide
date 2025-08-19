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

  - [explanation](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/blob/main/gof/creational/explanation.md)

  - [factory](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/factory)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/factory/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/factory/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/factory/solution.js)

  - [constructor](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/constructor)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/constructor/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/constructor/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/constructor/solution.js)

  - [singleton](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/singleton)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/singleton/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/singleton/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/singleton/solution.js)

  - [builder](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/builder)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/builder/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/builder/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/builder/solution.js)

  - [prototype](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/prototype)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/prototype/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/prototype/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/prototype/solution.js)

  - [abstract](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/abstract)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/abstract/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/abstract/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/creational/abstract/solution.js)

---

## Structural Design Patterns

These patterns focus on **class/object composition** and the relationships between objects.  
They allow you to add new functionalities to objects so that **restructuring some parts of the system does not affect the rest**.  
Hence, when some parts of the structure change, the entire system does not need to be modified.

- [structural](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural)

  - [explanation](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/blob/main/gof/structural/explanation.md)

  - [decorator](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/decorator)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/decorator/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/decorator/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/decorator/solution.js)

  - [facade](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/facade)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/facade/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/facade/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/facade/solution.js)

  - [adapter](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/adapter)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/adapter/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/adapter/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/adapter/solution.js)

  - [bridge](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/bridge)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/bridge/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/bridge/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/bridge/solution.js)

  - [composite](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/composite)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/composite/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/composite/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/composite/solution.js)

  - [flyweight](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/flyweight)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/flyweight/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/flyweight/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/flyweight/solution.js)

  - [proxy](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/proxy)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/proxy/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/proxy/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/structural/proxy/solution.js)

---

## Behavioral Design Patterns

These patterns are concerned with **communication between dissimilar objects** in a system.  
They streamline communication and ensure that **information is synchronized** between such objects.

- [behavioral](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral)

  - [explanation](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/blob/main/gof/behavioral/explanation.md)

  - [chain-of-responsibility](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/chain-of-responsibility)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/chain-of-responsibility/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/chain-of-responsibility/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/chain-of-responsibility/solution.js)

  - [command](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/command)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/command/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/command/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/command/solution.js)

  - [iterator](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/iterator)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/iterator/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/iterator/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/iterator/solution.js)

  - [mediator](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/mediator)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/mediator/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/mediator/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/mediator/solution.js)

  - [observer](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/observer)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/observer/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/observer/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/observer/solution.js)

  - [visitor](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/visitor)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/visitor/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/visitor/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/behavioral/visitor/solution.js)

---

## Architectural Design Patterns

These patterns are used for **solving architectural problems** within a given context in software architecture.

- [architectural](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural)

  - [explanation](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/blob/main/gof/architectural/explanation.md)

  - [mvc](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvc)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvc/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvc/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvc/solution.js)

  - [mvp](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvp)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvp/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvp/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvp/solution.js)

  - [mvvm](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvvm)

    - [explanation.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvvm/explanation.md)
    - [problem.md](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvvm/problem.md)
    - [solution.js](https://github.com/Abdulmoiz-Ahmer/software-design-patterns/tree/main/gof/architectural/mvvm/solution.js)
