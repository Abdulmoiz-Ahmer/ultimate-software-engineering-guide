# Challenge: Composite Pattern

In this challenge, you have to implement the composite pattern to solve the given problem.

---

## Problem Statement

In this challenge, you have to implement a directory system using the composite pattern.

You have been given the following skeleton code:

```javascript
class Directory {
  constructor(name, lastModified, size) {
    this.name = name;
    this.lastModified = lastModified;
    this.size = size;
  }
  getLastmodified() {}
  getSize() {}
  getName() {}
}

class File extends Directory {}

class Folder extends Directory {}
```

It’s up to you to figure out which class will be the component, leaf subclass, and composite subclass.

A **Directory** has the following properties:

**name** : the name of the file/folder

**lastModified**: the time in minutes since the last modification

**size**: the size of the file/folder in kilobytes

You have the following functions in the **Directory** class:

**getLastmodified**: Returns the **lastModified** time of a file. In the case of a folder with multiple files, it should return the minimum of the **lastmodified** times of all files.

**getSize**: Returns the **size** of a file/folder.

**getName**: Returns the **name** of the file or all the files in the case of a folder.

The composite subclass should contain the following additional functions as well:

- addFile
- removeFile

### Input

Calling the given functions on files and folders

---

### Output

The correct output after calling these functions such as **lastModified** time, **name**, and **size**

### Sample input

```javascript
const file = new File("penguiny.png", 6, 12);
file.getLastmodified();
file.getName();
file.getSize();
```

### Sample output

```javascript
6;
("penguiny.png");
12;
```

### Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
//Component
class Directory {
  constructor(name, lastModified, size) {
    this.name = name;
    this.lastModified = lastModified;
    this.size = size;
  }
  getLastmodified() {}
  getSize() {}
  getName() {}
}

//Leaf subclass
class File extends Directory {}

//Composite subclass
class Folder extends Directory {}
```
