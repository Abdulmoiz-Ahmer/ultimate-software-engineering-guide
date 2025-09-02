# Challenge: Iterator Pattern

## Problem Statement

In this challenge, you have to reverse iterate a simple hashmap and display its key values.

You need to implement the **reverseIterate** function that accepts the hashmap, **items**, and displays the key values in reverse. To reverse iterate, make use of the **ReverseIterator** class. It contains the following functions:

- **hasprevElement**: checks if there is a previous element

- **last**: returns the last key value in the map

- **previous**: returns the previous key value in the map

Apart from the functions mentioned above, you also need to define its constructor.

---

## Input

Calling **reverseIterate** function on a simple hashmap

---

## Output

Hashmap’s values displayed in reverse order

---

## Sample Input

```javascript
reverseIterate({
  name: "Anne",
  age: "23",
  gender: "Female",
  Occupation: "Engineer",
});
```

## Sample Output

```javascript
"Engineer";
"Female";
"23";
"Anne";
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class ReverseIterator {
  //define-your-reverse-iterator-here
  hasprevElement() {}
  last() {}
  previous() {}
}

function reverseIterate(items) {
  //write-your-code-here
  //to display the values of keys
  //in items in reverse
  console.log(items);
}
```
