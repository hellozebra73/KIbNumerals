import React, { Component } from "react";
import PropTypes from "prop-types";
import MathInputs from "./MathInputs";
import csrfToken from "./util/csrf";
import "./Solution.css"

// Component for students to enter answers
class SolutionNumeral extends Component {
  constructor(props) {
    super(props);

    this.state = {
    };

  }

  // Hint clicked, call handler in parent


  // Input changed
  render() {
    const { feedback } = this.state;
    const{numeral, numeralPos }=this.props;
    const steps=(numeral.steps.length>0)?numeral.steps:[];
    const expanded=true;

    return (
      <div>
      <MathInputs  numeralPos={numeralPos} step={0} onChange={this.props.onChange} />
      {steps.map((step) => (
        <div className="ans_field" key={`step-${step.step_number}`}>

            {expanded && (
              <div>
                <p className="ot fade-in">
                  <span className="ot">{step.step_number}) </span>
                  <span className="ot">{step.instruction}</span>
                </p>
                <MathInputs  numeralPos={numeralPos} step={step.step_number} hint={step.hint} onChange={this.props.onChange} />
              </div>
            )}
        </div>
      ))}
      </div>

            );
          }
};



export default SolutionNumeral;
