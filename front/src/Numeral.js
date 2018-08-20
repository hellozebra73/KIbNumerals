import React, { Component } from "react";
import PropTypes from "prop-types";
import Math from "./Math";
import Steps from "./Steps";

// A single step
class Numeral extends Component {
  constructor(props) {
    super(props);

    this.state = {
      expanded: false,
      current: 0,
      steps: [],
    };


  }

  onExpand(step) {

    const { onExpand } = this.props;

    if (onExpand) {
      onExpand(step);
    }
  }

  // Open/close step


  render() {
  const{numeral}=this.props;
  const { activeNumeral,  numerals, currentNumerals } = this.props;
  const steps=(typeof activeNumeral!= "undefined")?activeNumeral.steps:[];
  console.log(numeral);
    return (
      <div>
            <br/>

            <Steps numeral={numeral} currentNumerals={currentNumerals} steps={steps}  onExpand={this.onExpand.bind(this)} />
      </div>
    );
  }
};



export default Numeral;
