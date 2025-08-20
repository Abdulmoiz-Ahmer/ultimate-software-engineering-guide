class LibraryKiosk {
  open(app) {
    console.log(`Opening ${app}`);
  }
  connectTo(website) {
    console.log("Connecting to " + website);
  }
}

class ProxyLibraryKiosk {
  constructor() {
    this.libraryKiosk = new LibraryKiosk();
    this.blockedSites = [
      "fb.com",
      "instagram.com",
      "snapchat.com",
      "google.com",
      "gmail.com",
    ];
    this.blockedApps = ["camera", "photos", "music", "settings"];
  }

  open(app) {
    if (this.blockedApps.includes(app)) {
      console.log(`You can't access the ${app}`);
    } else {
      this.libraryKiosk.open(app);
    }
  }
  connectTo(website) {
    if (this.blockedSites.includes(website)) {
      console.log(`Access to ${website} denied`);
    } else {
      this.libraryKiosk.connectTo(website);
    }
  }
}

var libraryKiosk = new ProxyLibraryKiosk();
libraryKiosk.open("photos");
libraryKiosk.open("Chrome");
libraryKiosk.connectTo("booksportal.com");
libraryKiosk.connectTo("google.com");
