let configure = null;
class ConfigureVals {
  constructor(initvalues) {
    this.xpoint = initvalues.xpoint || 0;
    this.ypoint = initvalues.ypoint || 0;
    this.shape = initvalues.shape || null;
  }
  static getConfiguration(initvalues) {
    if (!configure) {
      configure = new ConfigureVals(initvalues);
    }
    return configure;
  }
}

var configureObj1 = ConfigureVals.getConfiguration({
  xpoint: 8,
  ypoint: 9,
  shape: "rectangle",
});
console.log(configureObj1);
var configureObj2 = ConfigureVals.getConfiguration({
  xpoint: 2,
  ypoint: 4,
  shape: "circle",
});
console.log(configureObj2);
