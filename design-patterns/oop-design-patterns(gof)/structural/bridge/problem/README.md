# Challenge: Facade Pattern

In this challenge, you have to implement the facade pattern to solve the given problem.

---

## Problem Statement

Study the code given below and its output. Carefully look at the classes defined and try to understand the purpose of the program.

---

Run the code below to see its implementation:

```javascript
class Applications {
  constructor(name, type) {
    this.name = name;
    this.type = type;
  }
  display() {}
  displayMode() {}
}

class FacebookLightMode extends Applications {
  constructor(name, type) {
    super(name, type);
  }
  display() {
    console.log(`Welcome to Facebook for ${this.type}.`);
  }
  displayMode() {
    console.log("You are using facebook in light mode.");
  }
}

class FacebookDarkMode extends Applications {
  constructor(name, type) {
    super(name, type);
  }
  display() {
    console.log(`Welcome to Facebook for ${this.type}.`);
  }
  displayMode() {
    console.log("You are using facebook in dark mode.");
  }
}

class WhatsAppLightMode extends Applications {
  constructor(name, type) {
    super(name, type);
  }
  display() {
    console.log(`Welcome to Whatsapp for ${this.type}.`);
  }
  displayMode() {
    console.log("You are using whatsapp in light mode.");
  }
}

class WhatsAppDarkMode extends Applications {
  constructor(name, type) {
    super(name, type);
  }
  display() {
    console.log(`Welcome to Whatsapp for ${this.type}.`);
  }
  displayMode() {
    console.log("You are using whatsapp in dark mode.");
  }
}

const fbLight = new FacebookLightMode("Facebook", "Social Networking");
const whatsappDark = new WhatsAppDarkMode("Whatsapp", "Chatting");
fbLight.display();
fbLight.displayMode();
whatsappDark.display();
whatsappDark.displayMode();
```

To further clarify, the code above has one parent class Applications and four child classes:

- FacebookLightMode
- FacebookDarkMode
- WhatsAppLightMode
- WhatsAppDarkMode

You can see that two major things define these classes:

- the application name
- the color mode of the application

Your task is to modify the code using the bridge pattern so it can be run as follows:

```javascript
const fb = new Facebook("Facebook", "Social Networking");
const mode = new Mode(fb);
mode.darkMode();
fb.displayMode();

const whatsapp = new WhatsApp("Whatsapp", "Chatting");
const mode2 = new Mode(whatsapp);
mode2.lightMode();
whatsapp.displayMode();
```

---

### Input

Calling light mode/dark mode methods for an application

---

### Output

The message displayed on switching to a specific color mode

### Sample input

```javascript
const fb = new Facebook("Facebook", "Social Networking");
const mode = new Mode(fb);
mode.darkMode();
fb.displayMode();

const whatsapp = new WhatsApp("Whatsapp", "Chatting");
const mode2 = new Mode(whatsapp);
mode2.lightMode();
whatsapp.displayMode();
```

### Sample output

```javascript
"You are using facebook in dark mode.";
"You are using whatsapp in light mode.";
```

### Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class Applications {
  constructor(name, type) {
    this.name = name;
    this.type = type;
  }
  display() {}
  displayMode() {}
}

class FacebookLightMode extends Applications {
  constructor(name, type) {
    super(name, type);
  }
  display() {
    console.log(`Welcome to Facebook for ${this.type}.`);
  }
  displayMode() {
    console.log("You are using facebook in light mode.");
  }
}

class FacebookDarkMode extends Applications {
  constructor(name, type) {
    super(name, type);
  }
  display() {
    console.log(`Welcome to Facebook for ${this.type}.`);
  }
  displayMode() {
    console.log("You are using facebook in dark mode.");
  }
}

class WhatsAppLightMode extends Applications {
  constructor(name, type) {
    super(name, type);
  }
  display() {
    console.log(`Welcome to Whatsapp for ${this.type}.`);
  }
  displayMode() {
    console.log("You are using whatsapp in light mode.");
  }
}

class WhatsAppDarkMode extends Applications {
  constructor(name, type) {
    super(name, type);
  }
  display() {
    console.log(`Welcome to Whatsapp for ${this.type}.`);
  }
  displayMode() {
    console.log("You are using whatsapp in dark mode.");
  }
}
```
