const Ninja = function (name) {
  this.points = 100;
  this.name = name;
};

Ninja.prototype.punch = function (otherNinja) {
  if (otherNinja.points > 0 && this.points > 0) {
    otherNinja.points -= 20;
    return `${otherNinja.name}'s points are ${otherNinja.points}`;
  } else {
    return `Can't punch ${otherNinja.name}`;
  }
};

Ninja.prototype.kick = function (otherNinja) {
  if (otherNinja.points > 0 && this.points > 0) {
    otherNinja.points -= 50;
    return `${otherNinja.name}'s points are ${otherNinja.points}`;
  } else {
    return `Can't kick ${otherNinja.name}`;
  }
};

const ninja1 = new Ninja("Ninja1");
const ninja2 = new Ninja("Ninja2");
console.log(ninja1.kick(ninja2));
console.log(ninja2.punch(ninja1));
console.log(ninja1.kick(ninja2));
console.log(ninja1.punch(ninja2));
console.log(ninja2.kick(ninja1));
