var Login = React.createClass({
  mixins: [React.addons.LinkedStateMixin],
  getInitialState: function() {
    return {username: TokenAuth.getUsername(), password: '', message: ''};
  },
  handleLogin: function() {
    TokenAuth.login(this.state.username, this.state.password,
      function() {
        this.props.setView("undecided");
      }.bind(this),
      function(message) {
        if(error == 400) {
          this.setState({message: "Username or password are incorrect."});
        }
        else {
          this.setState({message: message});
        }
      }.bind(this)
    );
  },
  disabled: function() {
    return this.state.username == '' || this.state.password == ''
  },
  handleRegisterClick: function(event) {
    this.props.setView("registration");
  },
  render: function () {
    return (
      <div>
        <p class="text-centered">{this.state.message}</p>
        <input type="text" placeholder="User" valueLink={this.linkState('username')} />
        <input type="password" placeholder="Password" valueLink={this.linkState('password')} />
        <button onClick={this.handleLogin} disabled={this.disabled()}>Login</button>
        <a onClick={this.handleRegisterClick}>Register</a>
      </div>
    );
  }
});
