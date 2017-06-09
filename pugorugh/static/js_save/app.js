var PugOrUgh = React.createClass({
  displayName: "PugOrUgh",

  getInitialState: function () {
    return {
      userName: TokenAuth.getUsername()
    };
  },
  componentWillMount: function () {
    this.setView(TokenAuth.loggedIn() ? 'undecided' : "login");
  },
  setView: function (view) {
    switch (view) {
      case "liked":
      case "undecided":
      case "disliked":
        var component = React.createElement(Dog, { setView: this.setView, filter: view });
        break;
      case "preferences":
        var component = React.createElement(Preferences, { setView: this.setView });
        break;
      case "registration":
        var component = React.createElement(Registration, { setView: this.setView });
        break;
      case "login":
        var component = React.createElement(Login, { setView: this.setView });
        break;
    }

    this.setState({ view: component, viewName: view });
  },
  handleLogoutClick: function () {
    TokenAuth.logout(function () {
      this.setView("login");
    }.bind(this));
  },
  hideLogout: function () {
    return this.state.viewName == "login";
  },
  render: function () {
    return React.createElement(
      "div",
      null,
      React.createElement(
        "header",
        { className: "circle--header" },
        React.createElement(
          "div",
          { className: "bounds" },
          React.createElement(
            "div",
            { className: "circle--fluid" },
            React.createElement(
              "div",
              { className: "circle--fluid--cell circle--fluid--primary" },
              React.createElement(
                "ul",
                { className: "circle--inline" },
                React.createElement(
                  "li",
                  null,
                  React.createElement("img", { src: "static/icons/logo.svg", height: "60px" })
                )
              ),
              TokenAuth.loggedIn() ? React.createElement(
                "a",
                { onClick: this.handleLogoutClick, hidden: this.hideLogout() },
                "Logout ",
                TokenAuth.getUsername()
              ) : null
            ),
            React.createElement(
              "div",
              { className: "circle--fluid--cell circle--fluid--secondary" },
              React.createElement(
                "nav",
                { disabled: this.state.view == "" },
                React.createElement(
                  "ul",
                  { className: "circle--inline" },
                  React.createElement(
                    "li",
                    { className: this.state.viewName == "liked" ? "current-tab" : "" },
                    React.createElement(
                      "a",
                      { onClick: this.setView.bind(this, "liked") },
                      "Liked"
                    )
                  ),
                  React.createElement(
                    "li",
                    { className: this.state.viewName == "undecided" ? "current-tab" : "" },
                    React.createElement(
                      "a",
                      { onClick: this.setView.bind(this, "undecided") },
                      "Undecided"
                    )
                  ),
                  React.createElement(
                    "li",
                    { className: this.state.viewName == "disliked" ? "current-tab" : "" },
                    React.createElement(
                      "a",
                      { onClick: this.setView.bind(this, "disliked") },
                      "Disliked"
                    )
                  )
                )
              )
            )
          )
        )
      ),
      React.createElement(
        "div",
        { className: "bounds" },
        React.createElement(
          "div",
          { className: "grid-60 centered" },
          this.state.view
        )
      )
    );
  }
});

ReactDOM.render(React.createElement(PugOrUgh, null), document.getElementById("container"));