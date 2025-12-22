# 💛 Vanilla JavaScript

A comprehensive guide and resource list for mastering the fundamentals of the web, without frameworks or libraries.

## 📖 Table of Contents

- [What is Vanilla JS?](#what-is-vanilla-js)
- [Core Concepts](#core-concepts)
- [The DOM & Events](#the-dom--events)
- [Asynchronous JavaScript](#asynchronous-javascript)
- [Modern ES6+ Features](#modern-es6-features)
- [Under the Hood](#under-the-hood)
- [Performance & Patterns](#performance--patterns)

---

## What is Vanilla JS?

The usage of plain JavaScript without any additional libraries like jQuery, React, or Vue.

Vanilla JS is the foundation of the web. It is fast, lightweight, and cross-platform. Understanding Vanilla JS is crucial because frameworks come and go, but the core language standards (ECMAScript) remain. Mastering these fundamentals makes you a better engineer in _any_ framework.

## Core Concepts

1. **Execution Context & Scope**
   JavaScript doesn't just run; it runs inside an environment. Understanding Global vs. Function vs. Block scope, and how the "Hoisting" mechanism works, is the first step to avoiding bugs.

2. **Closures**
   A function bundled together with references to its surrounding state (the lexical environment). Closures allow data privacy and the creation of function factories. They are the backbone of many design patterns.

3. **Prototypal Inheritance**
   Unlike class-based languages (Java, C#), JavaScript uses prototypes. Objects inherit properties and methods directly from other objects via the prototype chain.

4. **The Event Loop**
   JavaScript is single-threaded, yet it handles asynchronous tasks (like fetching data) without freezing. The Event Loop monitors the Call Stack and the Callback Queue to coordinate execution.

---

## Concepts

### The DOM & Events

- **[Introduction to the DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)** - How the browser represents HTML.
- **[Event Bubbling and Capturing](https://javascript.info/bubbling-and-capturing)** - How events travel through the DOM tree.
- **[Event Delegation](https://davidwalsh.name/event-delegate)** - A pattern to handle events efficiently on multiple elements.
- **[Manipulating Documents](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Manipulating_documents)** - Creating, changing, and removing HTML elements.

### Asynchronous JavaScript

- **[Introducing Asynchronous JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Introducing)** - Why we need async.
- **[Using Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)** - The modern alternative to callback hell.
- **[Async/Await](https://javascript.info/async-await)** - Syntactic sugar that makes async code look synchronous.
- **[The Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)** - The modern standard for making network requests.

### Modern ES6+ Features

- **[Var, Let, and Const](https://www.freecodecamp.org/news/var-let-and-const-whats-the-difference/)** - Understanding variable declarations.
- **[Arrow Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions)** - Concise syntax and lexical `this`.
- **[Destructuring Assignment](https://javascript.info/destructuring-assignment)** - Unpacking arrays and objects into variables.
- **[Spread Syntax & Rest Parameters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax)** - Expanding and collecting iterables.
- **[JavaScript Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)** - Import and Export syntax.

### Under the Hood

- **[What the heck is the event loop anyway?](https://www.youtube.com/watch?v=8aGhZQkoFbQ)** - (Video) The definitive guide to the Event Loop.
- **[Hoisting in JavaScript](https://www.digitalocean.com/community/tutorials/understanding-hoisting-in-javascript)** - How the engine handles declarations before execution.
- **[The "this" keyword](https://dmitripavlutin.com/gentle-explanation-of-this-in-javascript/)** - A gentle explanation of how context works.
- **[Equality comparisons and sameness](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Equality_comparisons_and_sameness)** - The difference between `==`, `===`, and `Object.is`.

### Performance & Patterns

- **[Debouncing and Throttling](https://css-tricks.com/debouncing-throttling-explained-examples/)** - Optimizing function calls for scroll/resize events.
- **[Design Patterns in JS](https://www.patterns.dev/posts/classic-design-patterns/)** - Singleton, Module, Observer patterns in vanilla JS.
- **[Memory Leaks in JS](https://auth0.com/blog/four-types-of-leaks-in-your-javascript-code-and-how-to-get-rid-of-them/)** - Common causes and how to avoid them.

---
