var CheckboxGroup = React.createClass({
  title: React.PropTypes.node.isRequired,
  checkBoxes: React.PropTypes.arrayOf(function(propValue, key, componentName, location, propFullName) {
    if (!key.hasOwnProperty('label') || !key.hasOwnProperty('value')) {
      return new Error("'checkBoxes' items are missing properties for 'label' or 'value'");
    }
  }).isRequired,
  data: React.PropTypes.instanceOf(Set).isRequired,
  onChange: React.PropTypes.func.isRequired,
  atLeastOne: React.PropTypes.bool,
  getDefaultProps: function() {
    return {
      atLeastOne: false
    };
  },
  checkboxClicked: function(value, event) {
    if (event.target.checked) {
      this.props.data.add(value);
    } else {
      if(this.props.atLeastOne && this.props.data.size <= 1) {
        return;
      }
      this.props.data.delete(value);
    }
    this.props.onChange(this.props.data);
    this.setState();
  },
  render: function () {
    return (
      <div>
        <h5>{this.props.title}</h5>
        {this.props.checkboxes.map(function(p) {
          return <label>
            <input type="checkbox" checked={this.props.data.has(p.value)}
                   onChange={this.checkboxClicked.bind(this, p.value)} />
            <span className="label-body">{p.label}</span>
          </label>
        }, this)}
      </div>
    );
  }
});
