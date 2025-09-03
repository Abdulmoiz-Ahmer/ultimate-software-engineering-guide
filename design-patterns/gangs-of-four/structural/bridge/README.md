# What is the bridge pattern?

The bridge pattern allows separate components with separate interfaces to work together. It keeps an object’s interface separate from its implementation, allowing the two to vary independently.

An example is controlling an air conditioner with a remote. The air conditioners can be of different types and each of them is controlled by a different remote. The remotes can vary, that is, a new one with better features can be introduced, but that won’t make any changes to the air conditioner classes. The same goes the other way round. The bridge pattern allows input and output devices to work together but vary independently.

## Example

Now, let’s implement the air conditioners and remote controls example we discussed above.

```javascript
class SimpleRemoteControl {
  constructor(ac) {
    this.ac = ac;

    this.on = function () {
      this.ac.on();
    };

    this.off = function () {
      this.ac.off();
    };

    this.setTemperature = function (temp) {
      this.ac.setTemperature(temp);
    };
  }
}

class InverterRemoteControl {
  constructor(ac) {
    this.ac = ac;

    this.heat = function () {
      this.ac.heatOn();
    };

    this.cold = function () {
      this.ac.coldOn();
    };

    this.on = function () {
      this.ac.on();
    };

    this.off = function () {
      this.ac.off();
    };

    this.setTemperature = function (temp) {
      this.ac.setTemperature(temp);
    };
  }
}

class SimpleAC {
  constructor() {
    this.on = function () {
      console.log("Simple AC is on");
    };

    this.off = function () {
      console.log("Simple AC is off");
    };

    this.setTemperature = function (temp) {
      console.log(`Simple AC's cooling is set to ` + temp + " degrees");
    };
  }
}

class InverterAC {
  constructor() {
    this.setting = "cool";

    this.on = function () {
      console.log("Inverter AC is on");
    };

    this.off = function () {
      console.log("Inverter AC is off");
    };

    this.heatOn = function () {
      this.setting = "heat";
      console.log("Inverter AC's heating is on");
    };

    this.coldOn = function () {
      this.setting = "cool";
      console.log("Inverter AC's cooling is on");
    };

    this.setTemperature = function (temp) {
      if (this.setting == "cool") {
        console.log(`Inverter AC's cooling is set to ` + temp + " degrees");
      }
      if (this.setting == "heat") {
        console.log(`Inverter AC's heating is set to ` + temp + " degrees");
      }
    };
  }
}

const simpleAC = new SimpleAC();
const inverterAC = new InverterAC();

const simpleRemote = new SimpleRemoteControl(simpleAC);
const inverterRemote = new InverterRemoteControl(inverterAC);

simpleRemote.on();
simpleRemote.setTemperature(16);
simpleRemote.off();

inverterRemote.on();
inverterRemote.heat();
inverterRemote.setTemperature(22);
inverterRemote.off();
```

## Explanation

The example above shows how to implement the bridge pattern to make air conditioners and remote controls work together. As discussed above, the input (remote control) and the output device (air conditioner) are separate components. So, let’s start by looking at the air conditioner classes.

```javascript
class SimpleAC {
  constructor() {
    this.on = function () {
      console.log("Simple AC is on");
    };

    this.off = function () {
      console.log("Simple AC is off");
    };

    this.setTemperature = function (temp) {
      console.log(`Simple AC's cooling is set to ` + temp + " degrees");
    };
  }
}
```

SimpleAC is the commonly-used AC, designed to provide only cooling. Its functionalities include switching on/off and providing cooling at the temperature set.

```javascript
class InverterAC {
  constructor() {
    this.setting = "cool";
    //code...
    this.on = function () {
      console.log("Inverter AC is on");
    };

    this.off = function () {
      console.log("Inverter AC is off");
    };

    this.setTemperature = function (temp) {
      //code...
    };
  }
}
```

InverterAC is similar to the SimpleAC since its functionalities also include switching on/off, and providing cooling at the temperature set. Additionally, it can also offer heating depending on the setting chosen by the user. Let’s look at the additional code below:

```javascript
class InverterAC {
  constructor(){

   this.setting = "cool"

   //code...


   this.heatOn = function(){
     this.setting = "heat"
     console.log("Inverter AC's heating is on")
   };

   this.coldOn = function() {
     this.setting = "cool"
     console.log("Inverter AC's cooling is on")
   };


   this.setTemperature = function(temp) {
     if(this.setting == "cool"){
       console.log(`Inverter AC's cooling is set to ` + temp + ' degrees');
     }
     if(this.setting == "heat"){
       console.log(`Inverter AC's heating is set to ` + temp + ' degrees');
     }

   };
}
```

As you can see, it has heatOn and the coldOn methods to change the setting to heat or cool. The setTemperature method also shows the message depending on the setting.

Now, let’s look at the remote control classes:

```javascript
class SimpleRemoteControl {
  constructor(ac) {
    this.ac = ac;

    this.on = function () {
      this.ac.on();
    };

    this.off = function () {
      this.ac.off();
    };

    this.setTemperature = function (temp) {
      this.ac.setTemperature(temp);
    };
  }
}
```

SimpleRemoteControl takes an ac object and allows operations such as turning it on, off, and setting its temperature. We use it to control SimpleAC.

Let’s look at the second type of remote control:

```javascript
class InverterRemoteControl {
  constructor(ac) {
    this.ac = ac;

    this.heat = function () {
      this.ac.heatOn();
    };

    this.cold = function () {
      this.ac.coldOn();
    };

    this.on = function () {
      this.ac.on();
    };

    this.off = function () {
      this.ac.off();
    };

    this.setTemperature = function (temp) {
      this.ac.setTemperature(temp);
    };
  }
}
```

InverterRemoteControl takes the ac object and allows operations such as turning it on/off, turning on heat/cold mode, and setting its temperature. We use it to control an InverterAC.

Note that even if the remote control class changes, it won’t affect the AC class. The two different classes can efficiently work together. You can pass the ac object to your remote control class, which will then perform the operations discussed on it.

```javascript
//Example
const simpleAC = new SimpleAC();
const simpleRemote = new SimpleRemoteControl(simpleAC);
simpleRemote.on();
simpleRemote.setTemperature(16);
simpleRemote.off();
```

# When to use the facade pattern?

You can use the bridge pattern if you want to:

- extend a class in several independent dimensions

- change the implementation at run time

- share the implementation between objects

