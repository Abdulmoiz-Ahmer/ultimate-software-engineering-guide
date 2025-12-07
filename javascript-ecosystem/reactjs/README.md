# ⚛️ React.js

A comprehensive guide and resource list for mastering React.js, from fundamental concepts to advanced ecosystem libraries.

## 📖 Table of Contents

- [What is React?](#what-is-react)
- [Core Concepts](#core-concepts)
- [Higher Order Components](#higher-order-components)
- [React Hooks](#react-hooks)

---

## What is React?

A JavaScript library for building user interfaces.

React (maintained by Meta) is used to build single-page applications and mobile apps. It allows developers to create large web applications that can change data, without reloading the page. The main purpose of React is to be fast, scalable, and simple.

## Core Concepts

1. Component-Based Architecture
   React splits the UI into independent, reusable pieces called Components. Think of them like LEGO blocks. You build small components (like a button or a navigation bar) and assemble them to create complex pages.

2. Declarative Syntax
   You simply tell React what you want the UI to look like based on the current data (state), and React handles the how. When data changes, React efficiently updates and renders just the right components.

3. Virtual DOM
   Instead of manipulating the browser's slow DOM directly, React creates a "Virtual DOM" in memory. When state changes, it compares the new Virtual DOM with the old one (a process called "diffing") and only updates the specific parts of the real DOM that changed. This makes it incredibly fast.

4. JSX (JavaScript XML)
   React uses a syntax extension called JSX, which looks like HTML but lives inside JavaScript. It makes writing the structure of components intuitive.

---

## Concepts

### Core Mental Models

- **[Render and Commit](https://react.dev/learn/render-and-commit)** - What and how of react renders
- **[Why React Re-Renders](https://www.joshwcomeau.com/react/why-react-re-renders/)** - Why of react rerenders

### Higher Order Components

- **[Mastering React Memo](https://www.youtube.com/watch?v=DEPwA3mv_R8)** - When to use React memo

### React Hooks

- **[Referencing Values with Refs](https://react.dev/learn/referencing-values-with-refs)** - The escape hatch of react renders
- **[Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)** - Everything about effects
- **[You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)** -
- **[Removing Effect Dependencies](https://react.dev/learn/removing-effect-dependencies)** - How to get rid of effects dependencies
- **[A Complete Guide to useEffect](https://overreacted.io/a-complete-guide-to-useeffect/)** - The under the hood of the useEffect.
- **[Mastering React's useEffect](https://www.youtube.com/watch?v=dH6i3GurZW8/)** - Tips and techiniques to tame useEffect.
- **[When to useMemo and useCallback](https://kentcdodds.com/blog/usememo-and-usecallback)** - The under the hood of the usememo and use callback.
- **[Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)** - The under the hood of the usememo and use callback.

### Performance

- **[lazy](https://react.dev/reference/react/lazy)** - Lazy loading components

### Testing

- **[Static vs Unit vs Integration vs E2E Testing for Frontend Apps](https://kentcdodds.com/blog/static-vs-unit-vs-integration-vs-e2e-tests)** - Types of testing
- **[Mocking REST API in Unit Test Using MSW](https://www.thisdot.co/blog/mocking-rest-api-in-unit-test-using-msw)** - Mocking api server
- **[Seamless API Mocking in Tests with Mock Service Worker](https://leapcell.io/blog/seamless-api-mocking-in-tests-with-mock-service-worker)** - Mocking api server
- **[React Hooks Testing Library](https://react-hooks-testing-library.com/usage/basic-hooks)** - React hooks testing library
- **[Common mistakes with React Testing Library](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)** - What not to do when using rtl

---
