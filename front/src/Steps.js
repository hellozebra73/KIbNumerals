import React, { Component } from "react";
import PropTypes from "prop-types";
import Step from "./Step";


// Holds the steps
class Steps extends Component {
  // Child expanded, pass to parent handler
  onExpand(step) {
    const { onExpand } = this.props;

    if (onExpand) {
      onExpand(step);
    }
  }

  render() {

    const {steps, currentNumerals,  numerals } = this.props;
    const {explanation, num}=this.props.numeral;



    return (
      <div className="">



        <div id="steps" className="card-body collapse">
        <p>  {explanation}{num} help</p>
          {steps.map((step) => (
            <Step step={step} key={`step-${step.step_number
            }`} onExpand={this.onExpand.bind(this)} />
          ))}
        </div>
      </div>
    );
  }
};

Steps.defaultProps = {
  onExpand: null,
};

Steps.propTypes = {

  steps: PropTypes.arrayOf(PropTypes.shape({})).isRequired,
  onExpand: PropTypes.func,
};

export default Steps;
