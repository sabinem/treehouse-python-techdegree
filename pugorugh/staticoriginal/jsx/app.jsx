var PugOrUgh = React.createClass({
  getInitialState: function () {
    return {
      userName: TokenAuth.getUsername()
    };
  },
  componentWillMount: function() {
    this.setView(TokenAuth.loggedIn() ? 'undecided' : "login");
  },
  setView: function(view) {
    switch(view) {
      case "liked":
      case "undecided":
      case "disliked":
        var component = <Dog setView={this.setView} filter={view}/>;
        break;
      case "preferences":
        var component = <Preferences setView={this.setView} />;
        break;
      case "registration":
        var component = <Registration setView={this.setView} />;
        break;
      case "login":
        var component = <Login setView={this.setView} />;
        break;
    }

    this.setState({view: component, viewName: view});
  },
  handleLogoutClick: function() {
    TokenAuth.logout(function() {
      this.setView("login");
    }.bind(this));
  },
  hideLogout: function() {
    return this.state.viewName == "login";
  },
  render: function () {
    return (
      <div>
        <header className="circle--header">
          <div className="bounds">
            <div className="circle--fluid">
              <div className="circle--fluid--cell circle--fluid--primary">
                <ul className="circle--inline">
                  <li><img src="static/icons/logo.svg" height="60px"/></li>
                </ul>
                { TokenAuth.loggedIn() ? <a onClick={this.handleLogoutClick} hidden={this.hideLogout()} >Logout {TokenAuth.getUsername()}</a> : null }
              </div>
              <div className="circle--fluid--cell circle--fluid--secondary">
                <nav disabled={this.state.view == ""}>
                  <ul className="circle--inline">
                    <li className={this.state.viewName == "liked"? "current-tab" : "" }>
                      <a onClick={this.setView.bind(this, "liked")}>Liked</a>
                    </li>
                    <li className={this.state.viewName == "undecided"? "current-tab" : "" }>
                      <a onClick={this.setView.bind(this, "undecided")}>Undecided</a>
                    </li>
                    <li className={this.state.viewName == "disliked"? "current-tab" : "" }>
                      <a onClick={this.setView.bind(this, "disliked")}>Disliked</a>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </header>
        <div className="bounds">
          <div className="grid-60 centered">{ this.state.view }</div>
        </div>
      </div>
    );
  }
});

ReactDOM.render(
  <PugOrUgh />
  , document.getElementById("container"));
