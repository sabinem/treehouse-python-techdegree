var Registration = React.createClass({
  displayName: 'Registration',

  mixins: [React.addons.LinkedStateMixin],
  getInitialState: function () {
    return { user: '', password: '', message: '' };
  },
  handleRegistration: function () {
    TokenAuth.register(this.state.user, this.state.password, function () {
      TokenAuth.login(this.state.user, this.state.password, function () {
        this.props.setView("preferences");
      }.bind(this));
    }.bind(this), function (message) {
      this.setState({ message: message });
    }.bind(this));
  },
  disabled: function () {
    return this.state.user == '' || this.state.password == '' || this.state.password2 == '' || this.state.password != this.state.password2;
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
      React.createElement('input', { type: 'text', placeholder: 'User', valueLink: this.linkState('user') }),
      React.createElement('input', { type: 'password', placeholder: 'Password', valueLink: this.linkState('password') }),
      React.createElement('input', { type: 'password', placeholder: 'Verify Password', valueLink: this.linkState('password2') }),
      React.createElement(
        'button',
        { className: 'button', onClick: this.handleRegistration, disabled: this.disabled() },
        'Register'
      )
    );
  }
});