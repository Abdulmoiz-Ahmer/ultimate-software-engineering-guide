# Ultimate Software Engineering Guide

A comprehensive, hands-on resource for mastering software engineering -- from core principles and design patterns to algorithmic problem solving, system design, and AI engineering.

## Modules

### [Software Engineering Principles](software-engineering-principles/)

Foundational principles every developer should know, with JavaScript examples.

| Principle | Description |
|-----------|-------------|
| [SOLID](software-engineering-principles/solid/) | Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion |
| [DRY](software-engineering-principles/dry/) | Don't Repeat Yourself -- centralizing logic to eliminate duplication |
| [KISS](software-engineering-principles/kiss/) | Keep It Simple, Stupid -- favoring straightforward solutions |
| [YAGNI](software-engineering-principles/yagni/) | You Aren't Gonna Need It -- implementing only what's required now |

---

### [Software Design Patterns](software-design-patterns/)

Classic and modern design patterns with explanations, problem statements, and JavaScript solutions.

**[OOP Design Patterns (GoF)](software-design-patterns/oop-design-patterns(gof)/)**

| Category | Patterns |
|----------|----------|
| Creational | Factory, Constructor, Singleton, Builder, Prototype, Abstract |
| Structural | Decorator, Facade, Adapter, Bridge, Composite, Flyweight, Proxy |
| Behavioral | Chain of Responsibility, Command, Iterator, Mediator, Observer |
| Architectural | MVC, MVP, MVVM |

**[Functional Design Patterns](software-design-patterns/functional-design-patterns/)** -- Composition, immutability, higher-order functions (curated resources)

---

### [Problem Solving Patterns](problem-solving-patterns/)

Algorithmic problems categorized by pattern, with solutions in JavaScript and Python.

**Implemented patterns:**

| Pattern | Problems |
|---------|----------|
| [Two Pointers](problem-solving-patterns/two-pointers/) | Valid Palindrome, Word Abbreviation, 3-Sum, Remove Nth Node, Sort Colors, Reverse Words, LCA III, Strobogrammatic Number |
| [Fast & Slow Pointers](problem-solving-patterns/fast-and-slow-pointers/) | Circular Array Loop, Find the Duplicate Number, Linked List Cycle III |
| [Sliding Window](problem-solving-patterns/sliding-window/) | Longest Repeating Character Replacement |

**Planned patterns:** Merge Intervals, Two Heaps, K-way Merge, Top K Elements, Modified Binary Search, Subsets, Greedy, Backtracking, Dynamic Programming, Cyclic Sort, Topological Sort, Matrices, Stacks, Graphs, Tree DFS/BFS, Trie, Hash Maps, Union Find, and more (28 total).

---

### [System Design](system-design/)

An introductory guide to designing scalable, reliable systems.

Covers load balancers, SQL vs NoSQL databases, caching, message queues, CDNs, the CAP theorem, sharding, and microservices vs monolithic architecture.

---

### [JavaScript Ecosystem](javascript-ecosystem/)

Curated learning guides and projects for the JavaScript ecosystem.

| Section | Contents |
|---------|----------|
| [Vanilla JS](javascript-ecosystem/js/) | Core concepts, DOM & events, async JS, ES6+, performance patterns (resource guide) |
| [React.js](javascript-ecosystem/reactjs/) | Hooks, HOCs, performance, testing (resource guide) |
| [Data Grid](javascript-ecosystem/reactjs/data-grid/) | React 19 + Vite project demonstrating `useMemo`, `useCallback`, `React.memo`, sorting, and pagination |

---

### [AI Engineer](ai-engineer/)

A project-based curriculum for learning AI engineering, from LLM API calls to autonomous agents.

| # | Module | Status |
|---|--------|--------|
| 01 | [Foundations and Prompting](ai-engineer/01-foundations-and-prompting/) | Done |
| 02 | [Memory and Vector Databases](ai-engineer/02-memory-and-vector-dbs/) | Done |
| 03 | [Industry Frameworks](ai-engineer/03-industry-frameworks/) | Done |
| 04 | [Agents and Tools](ai-engineer/04-agents-and-tools/) | Done |
| 05 | [Multimodal AI](ai-engineer/05-multimodal-ai/) | Done |
| 06 | Agentic AI and Orchestration | Coming soon |
| 07 | Advanced RAG | Coming soon |
| 08 | Model Finetuning | Coming soon |
| 09 | LLMOps and Evaluation | Coming soon |
| 10 | MCP and Tool Infrastructure | Coming soon |
| 11 | UI and Deployment | Coming soon |

---

## Prerequisites

- **JavaScript/TypeScript** -- Node.js for design patterns and problem solving
- **Python 3.10+** -- For AI engineer modules and algorithm solutions
- **Ollama** -- With `llama3` pulled (AI engineer modules)
- **Gemini API key** -- For AI engineer module 01 ([Google AI Studio](https://aistudio.google.com/))

## License

This project is open source. See individual module READMEs for specific license details.
