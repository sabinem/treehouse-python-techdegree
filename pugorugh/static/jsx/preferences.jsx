var Preferences = React.createClass({
  data: {
    age: new Set(['b','y','a','s']),
    gender: new Set(['m','f']),
    size: new Set(['s','m','l','xl'])
  },
  getInitialState: function () {
    return { data: this.data };
  },
  componentDidMount: function() {
    this.serverRequest = $.ajax({
      url: "api/user/preferences/",
      method: "GET",
      dataType: "json",
      headers: TokenAuth.getAuthHeader()
    }).done(function(data) {
      this.data = {
        age: new Set(data.age? data.age.split(",") : ['b','y','a','s']),
        gender: new Set(data.gender? data.gender.split(",") : ['m','f']),
        size: new Set(data.size? data.size.split(",") : ['s','m','l','xl'])
      };
      this.setState({ data: data });
    }.bind(this));
  },
  componentWillUnmount: function() {
    this.serverRequest.abort();
  },
  handleCheckboxGroupDataChanged : function (property, data) {
    this.data[property] = data
  },
  save: function() {
    var json  = JSON.stringify({
      age: Array.from(this.data.age).join(','),
      gender: Array.from(this.data.gender).join(','),
      size: Array.from(this.data.size).join(',')
    });

    $.ajax({
      url: "api/user/preferences/",
      method: "PUT",
      dataType: "json",
      headers: $.extend({'Content-type': 'application/json'}, TokenAuth.getAuthHeader()),
      data: json,
      success: this.props.setView.bind(this, 'undecided')
    });
  },
  render: function () {
    return (
      <div>
        <h4>Set Preferences</h4>
        <CheckboxGroup
          title="Gender"
          checkboxes={[
            {label: "Male", value: "m"},
            {label: "Female", value: "f"}
          ]}
          data={this.state.data.gender}
          onChange={this.handleCheckboxGroupDataChanged.bind(this, 'gender')}
          atLeastOne={true}
        />
        <CheckboxGroup
          title="Age"
          checkboxes={[
            {label: "Baby", value: "b"},
            {label: "Young", value: "y"},
            {label: "Adult", value: "a"},
            {label: "Senior", value: "s"}
          ]}
          data={this.state.data.age}
          onChange={this.handleCheckboxGroupDataChanged.bind(this, 'age')}
          atLeastOne={true}
        />
        <CheckboxGroup
          title="Size"
          checkboxes={[
            {label: "Small", value: "s"},
            {label: "Medium", value: "m"},
            {label: "Large", value: "l"},
            {label: "Extra Large", value: "xl"}
          ]}
          data={this.state.data.size}
          onChange={this.handleCheckboxGroupDataChanged.bind(this, 'size')}
          atLeastOne={true}
        />
        <hr/>
        <button className="button" onClick={this.save}>Save</button>
      </div>
    );
  }
});
