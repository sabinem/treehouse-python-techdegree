var Dog = React.createClass({
  getInitialState: function () {
    return {filter: this.props.filter};
  },
  componentDidMount: function() {
    this.getFirst();
  },
  componentWillUnmount: function() {
    this.serverRequest.abort();
  },
  componentWillReceiveProps: function(props) {
    this.setState({details: undefined, message: undefined, filter: props.filter}, this.getNext);
  },
  getNext: function () {
    this.serverRequest = $.ajax({
      url: `api/dog/${ this.state.details ? this.state.details.id : -1 }/${ this.state.filter }/next/`,
      method: "GET",
      dataType: "json",
      headers: TokenAuth.getAuthHeader()
    }).done(function(data) {
      this.setState({details: data, message: undefined});
    }.bind(this))
      .fail(function (response) {
        var message = null;
        if (response.status == 404) {
          if (this.state.filter == "undecided") {
            message = "No dogs matched your preferences.";
          } else {
            message = `You don't have any ${this.state.filter} dogs.`;
          }
        } else {
          message = response.error;
        }
        this.setState({ message: message, details: undefined});
    }.bind(this));
  },
  changeDogStatus: function (newStatus) {
    this.serverRequest = $.ajax({
      url: `api/dog/${ this.state.details.id }/${ newStatus }/`,
      method: "PUT",
      dataType: "json",
      headers: TokenAuth.getAuthHeader()
    }).done(function (data) {
        this.getNext();
      }.bind(this))
      .fail(function (response) {
        this.setState({ message: response.error });
      }.bind(this));
  },
  getFirst: function() {
    this.getNext();
  },
  handlePreferencesClick: function(event) {
    this.props.setView("preferences");
  },
  genderLookup: {m: 'Male', f: 'Female'},
  sizeLookup: {s: 'Small', m: 'Medium', l: 'Large', xl: 'Extra Large'},
  dogControls: function() {
    var like = <a onClick={this.changeDogStatus.bind(this, 'liked')}><img src="static/icons/liked.svg" height="45px" /></a>;
    var dislike = <a onClick={this.changeDogStatus.bind(this, 'disliked')}><img src="static/icons/disliked.svg" height="45px" /></a>;
    var undecide = <a onClick={this.changeDogStatus.bind(this, 'undecided')}><img src="static/icons/undecided.svg" height="45px" /></a>;
    var next = <a onClick={this.getNext}><img src="static/icons/next.svg" height="45px" /></a>;

    switch(this.state.filter) {
      case "liked":
        return (
          <p className="text-centered dog-controls">
            {dislike}
            {undecide}
            {next}
          </p>
        );
      case "disliked":
        return (
          <p className="text-centered dog-controls">
            {like}
            {undecide}
            {next}
          </p>
        );
      case "undecided":
        return (
          <p className="text-centered dog-controls">
            {dislike}
            {like}
            {next}
          </p>
        );
    }
  },
  contents: function() {
    if(this.state.message !== undefined) {
      return (
        <div>
          <p className="text-centered">{this.state.message}</p>
        </div>
      );
    }

    if(this.state.details === undefined) {
      return (
        <div>
          <p className="text-centered">Retrieving dog details...</p>
        </div>
      );
    }

    if(!this.state.details) {
      return (
        <div>
          <p className="text-centered">There are no more dogs to view. Please come back later.</p>
          <p className="text-centered">
            <a onClick={this.getFirst}>Start from beginning</a>
          </p>
        </div>
      );
    }

    return (
      <div>
        <img src={"static/images/dogs/" + this.state.details.image_filename} />
        <p className="dog-card">
          {this.state.details.name}&bull;
          {this.state.details.breed}&bull;
          {this.state.details.age} Months&bull;
          {this.genderLookup[this.state.details.gender]}&bull;
          {this.sizeLookup[this.state.details.size]}
        </p>
        {this.dogControls()}
      </div>
    );
  },
  render: function () {
    return (
      <div>
        {this.contents()}
        <p className="text-centered"><a onClick={this.handlePreferencesClick}>Set Preferences</a></p>
      </div>
    );
  }
});
