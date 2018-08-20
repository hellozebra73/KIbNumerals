import React, { Component } from "react";
import PropTypes from "prop-types";
import MathInput from "./MathInput";
import "./MathInput.css";

// Collection of MathInput
class MathInputs extends Component {
  constructor(props) {
    super(props);

    this.state = {
      fields: 1,
      answers: [],
    };

    this.onEnter = this.onEnter.bind(this);
    this.onChange = this.onChange.bind(this);
  }

  // Enter click on child input
  onEnter() {
    let { fields } = this.state;

    this.setState({ fields: fields + 1 });
  }

  // Child input changed
  onChange(index, math) {
    const { answers } = this.state;
    const { step, onChange , numeralPos} = this.props;
    answers[index] = math;
      
    this.setState({ answers });

    if (onChange) {
      onChange(numeralPos,step, answers);
    }
  }

  render() {
    const { fields } = this.state;
    const { step, hint } = this.props;

    return (
      <div>
        {hint && (
          <div className="math-input-container">
            <MathInput index={0} onEnter={this.onEnter} math={hint} />
          </div>
        )}
        {[...Array(fields).keys()].map((_, index) => (
          <div key={`mq-${step}-${index}`} className="math-input-container">
            <MathInput index={index} onEnter={this.onEnter} onChange={this.onChange} />
          </div>
        ))}
      </div>
    );
  }
};

MathInputs.defaultProps = {
  hint: null,
  onChange: null,
};

MathInputs.propTypes = {
  step: PropTypes.number.isRequired,
  hint: PropTypes.string,
  onChange: PropTypes.func,
};

export default MathInputs;
