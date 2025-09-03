# Challenge: Command Pattern

## Problem Statement

```javascript
class BankAccount {
  constructor(amount) {
    this.amount = amount;
  }

  checkAmount() {
    console.log(this.amount);
  }

  withdrawMoney(withdrawamount) {
    if (withdrawamount > this.amount) {
      console.log("Not enough money");
    } else {
      this.amount -= withdrawamount;
    }
  }
  depositAmount(money) {
    this.amount += money;
  }
}

var account = new BankAccount(100);
account.checkAmount();
account.withdrawMoney(10);
account.checkAmount();
account.depositAmount(50);
account.checkAmount();
```

In the code above, you have a **BankAccount** class. You can check the **amount** in the account using the **checkAccount** function, withdraw a certain amount using the **withdrawMoney** function, and deposit an amount using the **depositAmount** function.

Your task is to modify the code above by using the command pattern. Remember, the pattern has the following parts:

- **commands**: **WithDraw**, **DepositAmount**, and **CheckAmount**

- **receiver**: **BankAccount**

- **invoker**: an **AccountManager** carrying out the operations requested using a request function

Use your knowledge of the pattern to divide your code into these objects.

---

## Input

Sending commands to carry out operations such as **withdrawMoney**, **checkAmount**, and **depositAmount**

---

## Output

The **amount** in the account after operations are performed

---

## Sample Input

```javascript
const manager = new AccountManager();
const account = new BankAccount(100);
const check = new CheckAmount(account);
manager.request(check);
const withdraw = new WithDrawAmount(account);
const deposit = new DepositAmount(account);
manager.request(withdraw, 10);
manager.request(check);
manager.request(deposit, 50);
manager.request(check);
```

## Sample Output

```javascript
100;
90;
140;
```

## Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
class BankAccount {
  constructor(amount) {
    this.amount = amount;
  }

  checkAmount() {
    console.log(this.amount);
  }

  withdrawMoney(withdrawamount) {
    if (withdrawamount > this.amount) {
      console.log("Not enough money");
    } else {
      this.amount -= withdrawamount;
    }
  }
  depositAmount(money) {
    this.amount += money;
  }
}
```
