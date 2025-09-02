# Challenge: MVP Pattern

In this challenge, you have to implement the MVP pattern to solve the given problem.

---

## Problem Statement

In this challenge, you need to implement sending and displaying a sent email using the MVP pattern. You have already been given the dummy code for the classes you need to implement.

The **Model** class should contain the following:

- The properties: sender’s name, receiver’s name, and the email title
- The get and set functions to access and set the values of each property

In the **View** class, you need to do the following:

- Define the **sendEmail** function to send an email

In the **Presenter** class, you need to do the following:

- Define the **setModel** function that sets the model
- Define the **getView** function to return the view
- Define the **sendEmail** function that sets the properties of the email and displays the email information

---

## **Input**

The sendEmail function is called

## **Output**

The information of the email is displayed

---

## **Sample Input**

```javascript
var model = new Model();
var view = new View();
var presenter = new Presenter(view);
presenter.setModel(model);
view.registerWith(presenter);
presenter.getView().sendEmail("Rachel", "Joey", "Rent Discussion");
presenter.getView().sendEmail("Monica", "Phoebe", "Smelly Cat Draft");
```

## Sample Output

```javascript
"Email From: Joey To: Rachel Title: Rent Discussion";
"Email From: Phoebe To: Monica Title: Smelly Cat Draft";
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class Model {
  //write your code here
}

class View {
  constructor() {
    this.presenter = null;
  }

  registerWith(presenter) {
    this.presenter = presenter;
  }

  sendEmail(to, fromWhom, emailTitle) {
    //write code here
  }

  displayEmailInfo(senderName, recieverName, emailTitle) {
    console.log(
      "Email From: " +
        senderName +
        " To: " +
        recieverName +
        " Title: " +
        emailTitle
    );
  }
}

class Presenter {
  constructor(view) {
    this.view = view;
    this.model = null;
  }

  setModel(model) {
    //write code here
  }

  getView() {
    //write code here
  }

  sendEmail(to, fromWhom, emailTitle) {
    //write your code here
  }
}
```
