class SuperHero {
  constructor(name,power) {
    this.name = name
    this.power = power
  }
}

function SuperHeroWithSword(superhero){
    superhero.sword = true
    superhero.hasSword= function(){
    return `${this.name}'s power is ${this.power}, and he also has a sword now.`
  }
  return superhero;
} 

function SuperHeroWithSuperSpeed(superhero) {
    superhero.superSpeed = true
    superhero.hasSuperSpeed= function(){
    return `${this.name}'s power is ${this.power}, and he also has the super speed now.`
  }
  return superhero;
}

function SuperHeroWithSpeedandSword(superhero){
    superhero.speedAndSword = true
  
  superhero.hasSpeedAndSword = function(){
    return `${this.name}'s power is ${this.power}, and he also has both super speed and a sword now.`
  }
  return superhero;
}

var superhero1 = new SuperHero("Fire Man", "Fire")
SuperHeroWithSword(superhero1)
console.log(superhero1.hasSword())
SuperHeroWithSuperSpeed(superhero1)
console.log(superhero1.hasSuperSpeed())
var superhero2 = new SuperHero("Ice Man", "Ice")
SuperHeroWithSpeedandSword(superhero2)
console.log(superhero2.hasSpeedAndSword())