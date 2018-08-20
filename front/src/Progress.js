import React from "react";
import PropTypes from "prop-types";

// Progress bar
const Progress = ({ progress }) => (
  <div className="progress">
    <div
      id="pbar"
      className="progress-bar"
      role="progressbar"
      aria-valuenow="0"
      aria-valuemin="0"
      aria-valuemax="100"
      style={{ width: `${progress}%` }}
    >
      {progress > 0 && `${progress}%`}
    </div>
  </div>
);

Progress.defaultProps = {};

Progress.propTypes = {
  progress: PropTypes.number.isRequired,
};

export default Progress;
