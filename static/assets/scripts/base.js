class API {
  constructor() {
    this.url = window.location.href.trimEnd("/") + "/api";
  }
  getUrl() {
    return this.url;
  }
  makeUrl(path) {
    if (!path.startsWith("/")) {
      throw new Error("Path must start with /");
    }
    return this.url + path;
  }
}