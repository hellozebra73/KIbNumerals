import React from "react";
import ReactDOM from "react-dom";
import "bootstrap";
import Problem from "./Problem";
import Create from "./Create";
import registerServiceWorker from "./registerServiceWorker";
import "./index.css";

registerServiceWorker();

const components = {
  'Problem': Problem,
  'Create': Create,
};

document.querySelectorAll('[data-react-component]').forEach((element) => {

  const Component = components[element.dataset.reactComponent];
  const propsStr = element.dataset.reactProps;
  const props = propsStr ? JSON.parse(propsStr) : {};

  ReactDOM.render(<Component {...props} />, element);
});
