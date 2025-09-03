class ReverseIterator {
  constructor(elements) {
    this.keys = Object.keys(elements);
    this.index = this.keys.length - 1;
    this.elements = elements;
  }

  hasprevElement() {
    return this.index >= 0;
  }

  last() {
    this.index = this.keys.length - 1;
    return this.elements[this.keys[this.index]];
  }

  previous() {
    if (this.index >= 0) {
      return this.elements[this.keys[--this.index]];
    } else {
      return null;
    }
  }
}

function reverseIterate(items) {
  var iter = new ReverseIterator(items);

  for (var i = iter.last(); iter.hasprevElement(); i = iter.previous()) {
    console.log(i);
  }
}
