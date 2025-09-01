# Challenge: MVVM Pattern

## Problem Statement

In this challenge, you need to use the MVVM pattern to change the color of the “color” you write in the input field.

In the **Model**, you need to define the following functions:

- **subscribe**: Registers an observer
- **notifyObservers**: Notifies the observer of a change
- **getCurrentColor**: Returns the current color
- **setColor**: Sets a new color

In the **ViewModel**, you need to define the **bind** function, which reflects changes made in the view on the model and vice versa. It should do the following as well:

If you write **green** in the input, the color of the text **green** should change to **red**

If you write **red** in the input, the color of the text **red** should change to **blue**

If you write **blue** in the input, the color of the text **blue** should change to **green**

The view is provided to you in the form of the HTML code. Study it carefully before writing the JavaScript code.

---

## Input

The name of the color

---

## Output

The color of the text changes to green, red, or blue according to the rules given

---

## Sample Input

```javascript
green;
red;
blue;
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```html
<html>
  <head> </head>
  <body>
    Color: <input type="text" name="color" id="color" />
  </body>
  <script src="index.js" type="text/javascript"></script>
  <html></html>
</html>
```

```javascript
class Model {}

class ViewModel {}

var nameInput = document.getElementById("color");
var model = new Model();
var viewModel = new ViewModel(model);
viewModel.bind(nameInput, "color");
```
