var Dog = React.createClass({
  displayName: "Dog",

  getInitialState: function () {
    console.log("initial state dogs");
    return {
      filter: this.props.filter,
      dogs_for_filter_found: false
    };
  },
  componentDidMount: function () {
    this.getFirst();
  },
  componentWillUnmount: function () {
    this.serverRequest.abort();
  },
  componentWillReceiveProps: function (props) {
    console.log("dogs receiving props");
    this.setState({
      details: undefined,
      message: undefined,
      filter: props.filter,
      dogs_for_filter_found: false
    }, this.getNext);
  },
  getNext: function () {
    this.serverRequest = $.ajax({
      url: `api/dog/${this.state.details ? this.state.details.id : -1}/${this.state.filter}/next/`,
      method: "GET",
      dataType: "json",
      headers: TokenAuth.getAuthHeader()
    }).done(function (data) {
      this.setState({
        details: data,
        message: undefined,
        dogs_for_filter_found: true
      });
    }.bind(this)).fail(function (response) {
      var message = null;
      if (response.status == 404) {
        //message = "No dogs matched your preferences.";
        message = `You don't have any ${this.state.filter} dogs that fits your preference.`;
      } else {
        message = response.error;
      }
      this.setState({ message: message, details: undefined });
    }.bind(this));
  },
  changeDogStatus: function (newStatus) {
    this.serverRequest = $.ajax({
      url: `api/dog/${this.state.details.id}/${newStatus}/`,
      method: "PUT",
      dataType: "json",
      headers: TokenAuth.getAuthHeader()
    }).done(function (data) {
      this.getNext();
    }.bind(this)).fail(function (response) {
      this.setState({ message: response.error });
    }.bind(this));
  },
  getFirst: function () {
    console.log("get first");
    this.setState({ dogs_for_filter_found: false });
    this.getNext();
  },
  handlePreferencesClick: function (event) {
    this.props.setView("preferences");
  },
  genderLookup: { m: 'Male', f: 'Female' },
  sizeLookup: { s: 'Small', m: 'Medium', l: 'Large', xl: 'Extra Large' },
  dogControls: function () {
    var like = React.createElement(
      "a",
      { onClick: this.changeDogStatus.bind(this, 'liked') },
      React.createElement("img", { src: "static/icons/liked.svg", height: "45px" })
    );
    var dislike = React.createElement(
      "a",
      { onClick: this.changeDogStatus.bind(this, 'disliked') },
      React.createElement("img", { src: "static/icons/disliked.svg", height: "45px" })
    );
    var undecide = React.createElement(
      "a",
      { onClick: this.changeDogStatus.bind(this, 'undecided') },
      React.createElement("img", { src: "static/icons/undecided.svg", height: "45px" })
    );
    var next = React.createElement(
      "a",
      { onClick: this.getNext },
      React.createElement("img", { src: "static/icons/next.svg", height: "45px" })
    );

    switch (this.state.filter) {
      case "liked":
        return React.createElement(
          "p",
          { className: "text-centered dog-controls" },
          dislike,
          undecide,
          next
        );
      case "disliked":
        return React.createElement(
          "p",
          { className: "text-centered dog-controls" },
          like,
          undecide,
          next
        );
      case "undecided":
        return React.createElement(
          "p",
          { className: "text-centered dog-controls" },
          dislike,
          like,
          next
        );
    }
  },
  contents: function () {
    if (this.state.message !== undefined && !this.state.dogs_for_filter_found) {
      return React.createElement(
        "div",
        null,
        React.createElement(
          "p",
          { className: "text-centered" },
          this.state.message
        )
      );
    }

    if (this.state.details === undefined && !this.state.dogs_for_filter_found) {
      return React.createElement(
        "div",
        null,
        React.createElement(
          "p",
          { className: "text-centered" },
          "Retrieving dog details..."
        )
      );
    }

    if (!this.state.details && this.state.dogs_for_filter_found) {
      return React.createElement(
        "div",
        null,
        React.createElement(
          "p",
          { className: "text-centered" },
          "There are no more dogs to view. Please come back later."
        ),
        React.createElement(
          "p",
          { className: "text-centered" },
          React.createElement(
            "a",
            { onClick: this.getFirst },
            "Start from beginning"
          )
        )
      );
    }

    return React.createElement(
      "div",
      null,
      React.createElement("img", { src: "static/images/dogs/" + this.state.details.image_filename }),
      React.createElement(
        "p",
        { className: "dog-card" },
        this.state.details.name,
        "\u2022",
        this.state.details.breed,
        "\u2022",
        this.state.details.age,
        " Months\u2022",
        this.genderLookup[this.state.details.gender],
        "\u2022",
        this.sizeLookup[this.state.details.size]
      ),
      this.dogControls()
    );
  },
  render: function () {
    return React.createElement(
      "div",
      null,
      this.contents(),
      React.createElement(
        "p",
        { className: "text-centered" },
        React.createElement(
          "a",
          { onClick: this.handlePreferencesClick },
          "Set Preferences"
        )
      )
    );
  }
});