## **What is the MVP Pattern?**

The **MVP pattern** stands for **Model-View-Presenter**.  
It is derived from the **MVP** pattern, but while **MVP** focuses on managing the **user interface**, **MVP** focuses on **improving the presentation logic**.

MVP consists of **three main components**:

### **1. Model**

- Provides the **data** that the application requires.
- Supplies the information that needs to be displayed in the **view**.

### **2. View**

- **Displays** data from the **model**.
- Passes **user actions** or **commands** to the **presenter**, which decides how to handle them.
- Does **not** contain business logic.

### **3. Presenter**

- Acts as the **middleman** between the **model** and the **view**.
- Retrieves data from the model, **processes or manipulates it**, and then returns it to the view for display.
- Handles **user interactions** received from the view.

---

## **MVP vs. MVP**

| Aspect            | **MVP**                                                                                | **MVC**                                                                                                                                                                                   |
| ----------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mediator**      | The **Controller** acts as the mediator between the **Model** and the **View**.        | The **Presenter** acts as the mediator between the **Model** and the **View**.                                                                                                            |
| **View Handling** | A **Controller** can manage **multiple views**.                                        | The **Presenter** usually has a **one-to-one mapping** with the **View**. If the view is complex, it can use **multiple presenters**.                                                     |
| **Communication** | The **View** can directly **observe** the **Model** for changes and **update itself**. | The **Model** and **View** are **completely separated**. The **Presenter** reacts to user actions, fetches and manipulates data from the **Model**, and updates the **View** accordingly. |

---

## Example

```javascript
class Model {
  constructor(text) {
    this.text = text;
  }
  setText(text) {
    this.text = text;
  }
  getText() {
    return this.text;
  }
}

class View {
  constructor() {
    this.presenter = null;
  }

  registerWith(presenter) {
    this.presenter = presenter;
  }

  displayError() {
    console.log("Text is not in upper case");
  }

  displayMessage(text) {
    console.log("The text is: " + text);
  }

  changeText(text) {
    this.presenter.changeText(text);
  }
}

class Presenter {
  constructor(view) {
    this.view = view;
    this.model = null;
  }

  setModel(model) {
    this.model = model;
  }

  getView() {
    return this.view;
  }

  changeText(text) {
    if (text !== text.toUpperCase()) {
      this.view.displayError();
    } else {
      this.model.setText(text);
      this.view.displayMessage(this.model.getText());
    }
  }
}

var model = new Model("Hello world!");
var view = new View();
var presenter = new Presenter(view);
presenter.setModel(model);
view.registerWith(presenter);
presenter.getView().changeText("unagi");
presenter.getView().changeText("UNAGI");
```

## Explanation

The example above implements the MVP pattern to display some text. It has three components, the **Model, View,** and **Presenter**. Let’s discuss them one by one.

**Model**

```javascript
class Model {
  constructor(text) {
    this.text = text;
  }
  setText(text) {
    this.text = text;
  }
  getText() {
    return this.text;
  }
}
```

The **Model** contains the data which includes the **text** to be displayed. It also has two functions: **setText** and **getText** to set and retrieve the **text** property.

**View**

```javascript
class View {
  constructor() {
    this.presenter = null;
  }

  registerWith(presenter) {
    this.presenter = presenter;
  }

  displayError() {
    console.log("Text is not in upper case");
  }

  displayMessage(text) {
    console.log("The text is: " + text);
  }

  changeText(text) {
    this.presenter.changeText(text);
  }
}
```

As discussed, the **View** is responsible for passing any user actions to the presenter. An example is that of the **changeText** function, which allows the user to change the text. As you can see, it notifies the **presenter**, which then calls the changeText function of its own. We will get into that when we discuss the **Presenter**. Similarly, the **View** also displays the updated data returned to it by the presenter. The **displayError** and **displayMessage** functions are defined for that purpose.

**Presenter**

```javascript
class Presenter {
  constructor(view) {
    this.view = view;
    this.model = null;
  }

  setModel(model) {
    this.model = model;
  }

  getView() {
    return this.view;
  }

  changeText(text) {
    if (text !== text.toUpperCase()) {
      this.view.displayError();
    } else {
      this.model.setText(text);
      this.view.displayMessage(this.model.getText());
    }
  }
}
```

As discussed, the **Presenter** is the channel of communication between the model and the **view**. Hence, it initializes the **view** in its **constructor** and uses the setModel function to initialize the model.

The presenter exposes the **getView** function to return the **view** set in the **constructor**. Now, if a user tries to change the text in the view mode, the **view** relays this action to the presenter, which then executes its **changeText** function.

**changeText** checks whether the **text** that the user wants to set is in the upper case or not. If it is, it updates the model and sets the new text. Since the model gets updated, the function returns the updated data to the view for display:

```javascript
this.model.setText(text);
this.view.displayMessage(this.model.getText());
```

However, if the **text** is not in the upper case, it calls the view to display the error.

```javascript
if(text !== text.toUpperCase()){
    this.view.displayError();
```

---

## When to Use the MVP Pattern?

- If your application requires a lot of reuse of the presentation logic
- If your application requires a lot of user interaction
- If your application has complex views
- For easier testing as the presenter can provide a mock interface that can be unit tested
