import React, { Component } from "react";
import PropTypes from "prop-types";
import MathQuill from "mathquill";

const MQ = MathQuill.getInterface(2);

// Renders a MathQuill input
class MathInput extends Component {
  componentDidMount() {
    const self = this;

    const input = MQ.MathField(this.input, {
      spaceBehavesLikeTab: true,
      handlers: {
        edit: function() {
          self.onChange(input.latex());
        }
      }
    });

    input.focus();

    this.input.addEventListener("keypress", this.onEnter.bind(this));
  }

  componentWillUnmount() {
    this.input.removeEventListener("keypress", this.onEnter);
  }

  // Handle input, call handler in parent
  onChange(math) {
    const { index, onChange } = this.props;

    if (onChange) {
      onChange(index, math);
    }
  }

  // Handle Enter key
  onEnter(event) {
    if (event.which === 13 && this.props.onEnter) {
      this.props.onEnter();
    }
  }

  render() {
    const { math } = this.props;

    return (
      <div className="math-input" ref={ref => this.input = ref}>
        {math}
      </div>
    );
  }
};

MathInput.defaultProps = {
  math: null,
  onEnter: null,
  onChange: null,
};

MathInput.propTypes = {
  index: PropTypes.number.isRequired,
  math: PropTypes.string,
  onEnter: PropTypes.func,
  onChange: PropTypes.func,
};

export default MathInput;
