import React, { Component } from "react";
import PropTypes from "prop-types";
import Math from "./Math";

// A single step
class Step extends Component {
  constructor(props) {
    super(props);

    this.state = {
      expanded: false,
    };

    this.onToggle = this.onToggle.bind(this);
  }

  // Open/close step
  onToggle() {
    const { expanded } = this.state;
    const { step, onExpand } = this.props;

    this.setState({ expanded: !expanded });

    if (!step.expanded && !expanded && onExpand) {
      onExpand(step.step);
    }
  }

  render() {
    const { step } = this.props;
    const { expanded } = this.state;

    return (
      <div>
        <button
          type="button"
          className="btn btn-info stepb bounce-top"
          onClick={this.onToggle}
        >
          <div className="numberCircle">
            <span>{step.step_number}</span>
          </div>
          <span>{step.step_name}</span>
        </button>
        <div
          className="scale-up-ver-top fade-in"
          style={{ display: expanded ? "block" : "none" }}
        >
          <Math math={step.explanation} />
        </div>
      </div>
    );
  }
};

Step.defaultProps = {
  onExpand: null,
};

Step.propTypes = {
  step: PropTypes.shape({}).isRequired,
  onExpand: PropTypes.func,
};

export default Step;
