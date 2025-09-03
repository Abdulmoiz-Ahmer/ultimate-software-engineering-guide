class Auctioneer {
  constructor() {
    this.bidderList = [];
  }

  announceNewBidderPrice() {
    this.notifyBidders();
  }

  registerBidder(bidder) {
    this.bidderList.push(bidder);
  }

  notifyBidders() {
    this.bidderList.forEach((bidder) => bidder.update());
  }
}

class Bidder {
  constructor(name) {
    this.name = name;
    this.bidPrice = null;
  }

  update() {
    console.log(`${this.name} is offering ${this.bidPrice} dollars`);
    if (this.bidPrice > 500) {
      console.log(`Sold to ${this.name}`);
    }
  }

  giveNewPrice(price) {
    this.bidPrice = price;
  }
}

auctioner = new Auctioneer();
bidder1 = new Bidder("Ross");
auctioner.registerBidder(bidder1);
bidder2 = new Bidder("Joey");
auctioner.registerBidder(bidder2);
bidder1.giveNewPrice(200);
bidder2.giveNewPrice(350);
auctioner.announceNewBidderPrice();
bidder1.giveNewPrice(400);
bidder2.giveNewPrice(550);
auctioner.announceNewBidderPrice();
