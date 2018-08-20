import React, { Component } from "react";
import PropTypes from "prop-types";
import Steps from "./Steps";
import Numeral from "./Numeral";
import "./GuideField.css"

// Holds the steps
class GuideField extends Component {
  // Child expanded, pass to parent handler
  constructor(props) {
      super(props);


  }


  onExpand(step) {

    const { onExpand } = this.props;

    if (onExpand) {
      onExpand(step);
    }
  }



  render() {
    const { currentNumerals,steps, currentStep, numerals } = this.props;
    const activeNumeral=currentNumerals[this.props.activeHelp];

    return (
      <div className="card card-default yellow">
      

          <div>
          <Numeral
                activeNumeral={activeNumeral}
                currentNumerals={currentNumerals}
                onExpand={this.onExpand.bind(this)}
                 steps={steps}
                numeral={this.props.numerals[this.props.activeHelp]}
                />
          </div>

      </div>
    );
  }
};



export default GuideField;
