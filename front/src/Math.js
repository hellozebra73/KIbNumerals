import React, { Component } from "react";
import PropTypes from "prop-types";
import renderMathInElement from "katex/contrib/auto-render/auto-render.js";

// Displays math using katex
class Math extends Component {
  componentDidMount() {
    renderMathInElement(this.explanation, {
      delimiters: [{ left: "$", right: "$", display: false }]
    });
  }

  render() {
    const { math } = this.props;

    return (
      <div
        className="step-panel"
        ref={ref => this.explanation = ref}
        dangerouslySetInnerHTML={{ __html: math }}
      />
    );
  }
};

Math.defaultProps = {
  onExpand: null,
};

Math.propTypes = {
  math: PropTypes.string.isRequired,
};

export default Math;
