var request = $;

var TokenAuth = {
  getAuthString() {
    return sessionStorage.getItem('authString');
  },
  setAuthString(authString) {
    sessionStorage.setItem('authString', authString);
  },
  clearAuthString() {
    sessionStorage.removeItem('authString');
  },
  getAuthHeader() {
    return { Authorization: "Token " + this.getAuthString() };
  },
  getUsername() {
    var username = localStorage.getItem("username");
    if (username) {
      return username;
    }
    return null;
  },
  setUsername(username) {
    localStorage.setItem("username", username);
  },
  login(username, password, successCallback, failCallback) {
    if (this.loggedIn()) {
      successCallback();
      return;
    }

    request
      .post('/api/user/login/', { username: username, password: password })
      .done(function(data) {
        this.setUsername(username);
        this.setAuthString(data.token);
        successCallback();
      }.bind(this))
      .fail(function(jqXHR, textStatus) {
        this.clearAuthString();
        failCallback(textStatus);
      }.bind(this));
  },
  logout(callback) {
    this.clearAuthString();
    callback();
  },
  loggedIn() {
    return !!this.getAuthString();
  },
  register(username, password, successCallback, failCallback) {
    request
      .post('/api/user/', { username: username, password: password })
      .done(function(data) {
        this.setUsername(username);
        successCallback();
      }.bind(this))
      .fail(function(jqXHR, textStatus) {
        failCallback(jqXHR.responseText);
      });
  }
};
