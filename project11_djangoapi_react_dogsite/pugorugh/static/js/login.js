var Login = React.createClass({
  displayName: 'Login',

  mixins: [React.addons.LinkedStateMixin],
  getInitialState: function () {
    return { username: TokenAuth.getUsername(), password: '', message: '' };
  },
  handleLogin: function () {
    TokenAuth.login(this.state.username, this.state.password, function () {
      this.props.setView("undecided");
    }.bind(this), function (message) {
      if (error == 400) {
        this.setState({ message: "Username or password are incorrect." });
      } else {
        this.setState({ message: message });
      }
    }.bind(this));
  },
  disabled: function () {
    return this.state.username == '' || this.state.password == '';
  },
  handleRegisterClick: function (event) {
    this.props.setView("registration");
  },
  render: function () {
    return React.createElement(
      'div',
      null,
      React.createElement(
        'p',
        { 'class': 'text-centered' },
        this.state.message
      ),
      React.createElement('input', { type: 'text', placeholder: 'User', valueLink: this.linkState('username') }),
      React.createElement('input', { type: 'password', placeholder: 'Password', valueLink: this.linkState('password') }),
      React.createElement(
        'button',
        { onClick: this.handleLogin, disabled: this.disabled() },
        'Login'
      ),
      React.createElement(
        'a',
        { onClick: this.handleRegisterClick },
        'Register'
      )
    );
  }
});