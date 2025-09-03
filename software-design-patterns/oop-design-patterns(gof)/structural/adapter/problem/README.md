# Challenge: Adapter Pattern

In this challenge, you have to implement the adapter pattern to solve the given problem.

---

## Problem Statement

In this challenge, you are given a TruthAndDare program like this:

Run the code below to see its implementation:

```javascript
// old interface
class TruthAndDare {
  constructor() {
    this.turn = Math.floor(Math.random() * 2) + 1;
  }
  Getturn() {
    if (this.turn == 1) {
      this.turn = 2;
    } else {
      this.turn = 1;
    }
    return this.turn;
  }
  playGame(playerOnename, playerTwoname) {
    if (this.Getturn() == 1) {
      return `${playerOnename}'s turn`;
    } else {
      return `${playerTwoname}'s turn`;
    }
  }
}

const obj = new TruthAndDare();
console.log(obj.playGame("Ross", "Chandler"));
```

There is a variable turn that decides which player’s turn it is to give a dare or ask a question. The Getturn() function is used to set and return the turn. It is set to either 1 or 2. The playGame function is simple: it takes two players and depending on the value of turn, returns the name of the player whose turn it is.

Now, as the creator of the game, you want to update the game. You want the turns to be random such that they are not limited to the values 1 or 2. So here’s what you want to change:

The turn value to be a random number. In the playGame function, if the turn is an even number, it’ll be player 1’s turn else it’ll be player 2’s turn. You name the updated function, newPlayGame.
Make a new interface for the updated functionality like so:

```javascript
// old interface
class TruthAndDare {
  constructor() {
    this.turn = Math.floor(Math.random() * 2) + 1;
  }
  Getturn() {
    if (this.turn == 1) {
      this.turn = 2;
    } else {
      this.turn = 1;
    }
    return this.turn;
  }
  playGame(playerOnename, playerTwoname) {
    if (this.Getturn() == 1) {
      return `${playerOnename}'s turn`;
    } else {
      return `${playerTwoname}'s turn`;
    }
  }
}

// new interface
class NewTruthAndDare {
  constructor(randomValue) {}

  newplayGame(playerOnename, playerTwoname) {
    //write-your-code-here
  }
}
```

One thing to note is that the players are used to using the playGame function and you want to quietly make the modifications without changing the outlook that the players are used to. For this purpose, you need to use the adapter pattern so that the players can keep on calling playGame, but the new functionality is implemented on the backend instead.

```javascript
// old interface
class TruthAndDare {
  constructor() {
    this.turn = Math.floor(Math.random() * 2) + 1;
  }
  Getturn() {
    if (this.turn == 1) {
      this.turn = 2;
    } else {
      this.turn = 1;
    }
    return this.turn;
  }
  playGame(playerOnename, playerTwoname) {
    if (this.Getturn() == 1) {
      return `${playerOnename}'s turn`;
    } else {
      return `${playerTwoname}'s turn`;
    }
  }
}

// new interface
class NewTruthAndDare {
  constructor(randomValue) {}

  newplayGame(playerOnename, playerTwoname) {
    //write-your-code-here
  }
}

// Adapter Class
class Adapter {
  constructor(randomValue) {
    //write-your-code-here
  }
}
```

### Input

Calling the **playGame** function

---

### Output

**newPlayGame** is invoked to decide the turn and the new message is shown to the players.

### Sample input

```javascript
const obj = new Adapter();
obj.playGame("Ross", "Channdler");
```

### Sample output

```javascript
"Rolling the dice";
```

### Challenge

Take a close look at this problem and design a step-by-step solution before jumping on to the implementation. This problem is designed for your practice, so try to solve it on your own first. If you get stuck, you can always refer to the solution provided. Good luck!

```javascript
// old interface
class TruthAndDare {
  constructor() {
    this.turn = Math.floor(Math.random() * 2) + 1;
  }
  Getturn() {
    if (this.turn == 1) {
      this.turn = 2;
    } else {
      this.turn = 1;
    }
    return this.turn;
  }
  playGame(playerOnename, playerTwoname) {
    if (this.Getturn() == 1) {
      return `${playerOnename}'s turn`;
    } else {
      return `${playerTwoname}'s turn`;
    }
  }
}

// new interface
class NewTruthAndDare {
  constructor(randomValue) {}

  newplayGame(playerOnename, playerTwoname) {
    //write-your-code-here
  }
}

// Adapter Class
class Adapter {
  constructor(randomValue) {
    //write-your-code-here
  }
}
```
