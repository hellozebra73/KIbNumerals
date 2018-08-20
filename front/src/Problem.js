import React, { Component } from "react";
import PropTypes from "prop-types";
import Steps from "./Steps";
import GuideField from "./GuideField";
import Solution from "./Solution";
import csrfToken from "./util/csrf";
import "./Problem.css";

const hints = [
  null,
  String.raw`a=\frac{\MathQuillMathField{y_2}-\MathQuillMathField{y_1}}{\MathQuillMathField{x_2}-\MathQuillMathField{x_1}}`
]

// Main components, holds steps and answers
class Problem extends Component {
  constructor(props) {
    super(props);

    this.state = {
      currentNumeral:0,
      currentStep:0,
      activeHelp:0,
      currentNumerals:[{help:false,name:"",steps:[]}],
      complete: 0,
      open: false,
    };
    this.numerals=[];
    JSON.parse(this.props.numerals).forEach((numeral) => (this.numerals.push(numeral.fields)));
    this.stepToState = this.stepToState.bind(this);
    this.onSteps = this.onSteps.bind(this);
    this.onExpand = this.onExpand.bind(this);
    this.onHint = this.onHint.bind(this);
    this.onNext = this.onNext.bind(this);
    this.onNumeralsHelp = this.onNumeralsHelp.bind(this);
    this.fetchStep = this.fetchStep.bind(this);
    this.nextNumeral = this.nextNumeral.bind(this);
  }





  componentDidMount() {

  let{currentNumerals}=this.state;
  currentNumerals[0].name=this.numerals[0].numeral_name;

  this.setState({ currentNumerals: currentNumerals });



  }

  // Show steps
  onSteps() {

    const { open} = this.state;

    if (!open) {
      //this.fetchNext();
      this.setState({ open: true });
    }


  }

stepToState(stepInfo,num,step){
let {currentNumerals}=this.state;
 currentNumerals[num].steps[step]=stepInfo
  this.setState({currentNumerals:currentNumerals});

}


 fetchStep(numeral,step){
   return   fetch(
      `/process_steps/?numeral_number=${numeral+1}&step_number=${step}&csrfmiddlewaretoken=${csrfToken()}`,
      {
        credentials: 'include',
      }
    ).then(response => response.json()).then(responseJson => this.stepToState(responseJson[0].fields,numeral,step))

  }

  onNumeralsHelp(num) {
    const { open,currentNumeral,currentNumerals, steps, } = this.state;
    this.setState({activeHelp:num});
    if(num===currentNumeral){
        if(currentNumerals[num].help===false){
            currentNumerals[num].help=true;
            this.fetchStep(num,1);
            this.setState({currentStep:1});

      }

      if (!open) {

        this.setState({ open: true });
      }
    }

  }

  // Step expanded
  onExpand(step) {
    const { steps } = this.state;
  //  const found = this.findStep(step);
    //found.expanded = true;

    this.setState({ steps: steps });

  }

  // Hint clicked
  onHint(step) {
    const { steps } = this.state;
    const found = this.findStep(step);

    if (!found) {
      return;
    }

    found.hint = hints[step];


    this.setState({ steps: steps });
  }

  nextNumeral(){
    let {currentNumerals, currentNumeral, currentStep  } = this.state;
      currentStep=0;
      currentNumeral=currentNumeral+1;
      let newNumeral={help:false,name:"",steps:[]};
      newNumeral.name=this.numerals[currentNumeral].numeral_name;
          console.log(currentNumerals);
      currentNumerals.push(newNumeral);
            console.log(currentNumerals);
      this.setState({currentStep});
      this.setState({currentNumeral});
      this.setState({currentNumerals});

  }
  onNext() {
    const {currentNumerals, currentNumeral,  complete } = this.state;
    let {currentStep}=this.state;
    const numberOfSteps=this.numerals[currentNumeral].number_of_steps;
    if (currentNumerals[currentNumeral].help==true){
      if (currentStep<numberOfSteps){
          currentStep=currentStep+1;
          this.setState({ currentStep: currentStep });
          this.fetchStep(currentNumeral,currentStep);
      }
      else  {this.nextNumeral();}
    }
    else  {this.nextNumeral();}
    //this.fetchNext();

    this.setState({ complete: complete + 1 });
  }
//fetchStep//



  render() {
    const { title, text, totalSteps  } = this.props;
    const { currentNumeral, currentStep, steps, complete, currentNumerals } = this.state;
    const numerals=this.numerals;


    return (
      <div className="problem">
        <div className="row">
          <div id="left-col" className="col-md-6">
            <div className="card trans">
               <div className="card-heading">
                 <h3 className=" trans"><span className="yellow-bot">{title}</span></h3>
               </div>
               <div className="card-body opaque37">
                 <p>{text}</p>
                 {numerals.map((numeral) => (

                   <p key={`hButton-${numeral.numeral_name}`}><span>{numeral.numeral_name})  </span>{numeral.question}</p>

                 ))}

               </div>

            </div>

            <div className="buttons">
            {currentNumerals.map((numeral,index) => (
                //HEre we set numeral_num
                  <button key={`hButton-${numeral.name}`}  className="btn button1 "
                    data-toggle="collapse"
                    data-target="#steps" onClick={()=>this.onNumeralsHelp(index)}>{"help "+numeral.name}</button>

            ))}
              </div>
               <br/>
            <GuideField

              steps={steps}
              onExpand={this.onExpand}
              onNumeralsHelp={this.onNumeralsHelp}
              currentNumerals={currentNumerals}
              activeHelp={this.state.activeHelp}
              numerals={numerals} />
          </div>
          <div className="col-md-6">
            <Solution
              currentStep={currentStep}
              steps={steps}
              progress={complete * 100/(totalSteps - 1)}
              onHint={this.onHint}
              onNext={this.onNext}
              numerals={numerals}
              currentNumerals={currentNumerals}
              currentNumeral={currentNumeral}

            />
          </div>
        </div>
      </div>
    );
  }
};

Problem.propTypes = {
  title: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  totalSteps: PropTypes.number.isRequired,
};

export default Problem;
