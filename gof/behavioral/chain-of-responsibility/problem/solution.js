class EmployeeChain {
  setNext(nextInChain) {}
  assignWork(req) {}
}

class Employee {
  constructor(name, level) {
    this.name = name;
    this.level = level;
  }

  getLevel() {
    return this.level;
  }

  getName() {
    return this.name;
  }
}

class EasyLevelWorkHandler extends EmployeeChain {
  constructor() {
    super();
    this.nextInChain = new EmployeeChain();
  }

  setNext(nextObj) {
    this.nextInChain = nextObj;
  }

  assignWork(req) {
    if (req.getLevel() == "Easy") {
      console.log("Easy work assigned to: " + req.getName());
    } else {
      this.nextInChain.assignWork(req);
    }
  }
}

class MediumLevelWorkHandler extends EmployeeChain {
  constructor() {
    super();
    this.nextInChain = new EmployeeChain();
  }

  setNext(nextObj) {
    this.nextInChain = nextObj;
  }

  assignWork(req) {
    if (req.getLevel() == "Medium") {
      console.log("Medium work assigned to: " + req.getName());
    } else {
      this.nextInChain.assignWork(req);
    }
  }
}

class HardLevelWorkHandler extends EmployeeChain {
  constructor() {
    super();
    this.nextInChain = new EmployeeChain();
  }

  setNext(nextObj) {
    this.nextInChain = nextObj;
  }

  assignWork(req) {
    if (req.getLevel() == "Hard") {
      console.log("Hard work assigned to: " + req.getName());
    } else {
      this.nextInChain.assignWork(req);
    }
  }
}

var w1 = new EasyLevelWorkHandler();
var w2 = new MediumLevelWorkHandler();
var w3 = new HardLevelWorkHandler();
w1.setNext(w2);
w2.setNext(w3);

const emp1 = new Employee("Joe", "Easy");
const emp2 = new Employee("Anne", "Medium");
const emp3 = new Employee("Shawn", "Hard");

w1.assignWork(emp1);
w1.assignWork(emp2);
w1.assignWork(emp3);
