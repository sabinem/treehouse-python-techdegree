var Registration = React.createClass({
  mixins: [React.addons.LinkedStateMixin],
  getInitialState: function() {
    return {user: '', password: '', message: ''};
  },
  handleRegistration: function() {
    TokenAuth.register(this.state.user, this.state.password,
      function() {
        TokenAuth.login(this.state.user, this.state.password, function () {
          this.props.setView("preferences");
        }.bind(this));
      }.bind(this),
      function(message) {
        this.setState({message: message});
      }.bind(this)
    );
  },
  disabled: function() {
    return this.state.user == '' || this.state.password == '' || this.state.password2 == '' ||
      this.state.password != this.state.password2;
  },
  render: function () {
    return (
      <div>
        <p class="text-centered">{this.state.message}</p>
        <input type="text" placeholder="User" valueLink={this.linkState('user')} />
        <input type="password" placeholder="Password" valueLink={this.linkState('password')} />
        <input type="password" placeholder="Verify Password" valueLink={this.linkState('password2')} />
        <button className="button" onClick={this.handleRegistration} disabled={this.disabled()}>Register</button>
      </div>
    );
  }
});
