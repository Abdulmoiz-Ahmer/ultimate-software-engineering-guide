# What is the Abstract Pattern?

To understand the abstract pattern, let’s go back to the factory pattern. We use the factory pattern to create multiple objects from the same family without having to deal with the creation process. The abstract pattern is similar; the difference is that it provides a constructor to create families of related objects. It is abstract, meaning it does not specify concrete classes or constructors.

For example, imagine we have an **Abstract Junk Food Factory** that can create either a **Chips Factory** or a **Soda Factory**. These two factories are different in what they produce, but they are related because they belong to the same overall category — junk food. Each factory then creates its own specific products, such as different types of chips or sodas.

---

## When to Use the Abstract Pattern?

The abstract pattern for creating instances is preferred over initializing when using the `new` operator since constructors have limited control over the process. Whereas, a factory will have broader knowledge.

**Use cases for this pattern include:**

- Applications requiring the reuse or sharing of objects
- Applications with complex logic because they have multiple families of related objects that need to be used together
- Object caching
- When the object creation process is to be shielded from the client
