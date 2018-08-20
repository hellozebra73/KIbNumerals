import React, { Component } from "react";
import PropTypes from "prop-types";
import MathInputs from "./MathInputs";
import Progress from "./Progress";
import SolutionNumeral from "./SolutionNumeral";
import Video from "./Video";
import csrfToken from "./util/csrf";
import "./Solution.css"

// Component for students to enter answers
class Solution extends Component {
  constructor(props) {
    super(props);

    this.state = {
      answers: [[]],
      feedback: null,
      loading: false,

    };

    this.OnNewNumeral = this.OnNewNumeral.bind(this);
    this.onHint = this.onHint.bind(this);
    this.onCheck = this.onCheck.bind(this);
    this.onChange = this.onChange.bind(this);
  }

  // Hint clicked, call handler in parent
  onHint() {
    const { onHint, currentStep } = this.props;

    if (onHint) {
      onHint(currentStep);
    }
  }
 //New numeral
 OnNewNumeral(){
   const{currentNumerals}=this.props;
   let nnum=true;
   if(currentNumerals[currentNumerals.length-1].help===true){
      if(currentNumerals[currentNumerals.length-1].steps.lenght<this.props.numerals[currentNumerals.length-1].number_of_steps){ nnum=false;}
}
if (nnum===true){
let {answers}=this.state;
answers.push([]);
this.setState({answers});}
}

  // Check answer
  onCheck() {
    const { answers, loading } = this.state;

    if (loading) {
      return;
    }

    const { currentNumeral,currentNumerals,currentStep, onNext } = this.props;

    const answer = answers[currentNumeral][currentStep];

    if (!answer) {
      return;
    }

    this.setState({ loading: true });

    const params = new URLSearchParams();
    params.append('csrfmiddlewaretoken', csrfToken());
    params.append('step_number', currentStep);
    params.append('numeral_number', currentNumeral);
    params.append('student_answer', JSON.stringify(answer));


    fetch(
      "/process/",
      {
        body: new URLSearchParams(params),
        method: "POST",
        credentials: 'include',
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
      }
    )
    .then(response => response.text())
    .then(responseText => {
      let feedback = "Vennligst prøv igjen!";
      if (responseText === "true") {
        feedback = "Riktig!!"

        if (onNext) {
          this.OnNewNumeral();
          onNext();
        }
      }

      this.setState({ feedback, loading: false });

      setTimeout(() => {
        this.setState({ feedback: null });
      }, 3000);
    })
  }

  // Input changed
  onChange(numeral, step, stepAnswers) {

    const { answers } = this.state;

      answers[numeral][step]=stepAnswers;
      this.setState({ answers });

  }

  render() {
    const { feedback } = this.state;
    const { currentStep, steps, progress ,numerals, currentNumerals} = this.props;

    console.log(this.props.numerals);



    return (
      <div className="solution">
        <div className="card-heading">
          <h3 className="yellow-text">Svarfelt</h3>
        </div>
        <div id="right-col" className="right-col trans">
          <div id="sv-felt" className="card trans">
            <div  className="card-body card-right opaque37">

            {currentNumerals.map((numeral,index)=>(
              <div key={`qS-${numeral.name}`}>
               <p className="ot fade-in"> Question {numeral.name}) </p>
              <SolutionNumeral  numeralPos={index} numeral={numeral} onChange={this.onChange}/>

              </div>
            ))}

            </div>
          </div>
          <Progress progress={progress} />

          <div className="buttons">
            <Video currentStep={currentStep} />
            <button type="button" className="btn button1" onClick={this.onHint}>Hint</button>
            <button type="button" className="btn button1" onClick={this.onCheck}>Sjekk svar</button>
          </div>

          <div className="beacon eqin2">
            {feedback}
          </div>
        </div>
      </div>
    );
  }
};

Solution.defaultProps = {
  onHint: null,
  onNext: null,
}

Solution.propTypes = {
  currentStep: PropTypes.number.isRequired,
  steps: PropTypes.arrayOf(PropTypes.shape({})).isRequired,
  progress: PropTypes.number.isRequired,
  onHint: PropTypes.func,
  onNext: PropTypes.func,
};

export default Solution;
