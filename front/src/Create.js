import React, { Component } from "react";
import ReactQuill, { Quill } from "react-quill";
import MathTheme from "./MathTheme";
import "./Create.css";

Quill.register('themes/math', MathTheme, true);

class Create extends Component {
  constructor(props) {
    super(props);
    this.state = { text: "" };
    this.handleChange = this.handleChange.bind(this);

    this.modules = {
      toolbar: {
        container: [
          [{ 'header': [1, 2, false] }],
          ['bold', 'italic', 'underline','strike', 'blockquote'],
          [{'list': 'ordered'}, {'list': 'bullet'}, {'indent': '-1'}, {'indent': '+1'}],
          ['link', 'image'],
          ['formula']
        ]
      }
    }
  }

  handleChange(value) {
    this.setState({ text: value });
  }

  render() {
    return (
      <ReactQuill value={this.state.text}
                  modules={this.modules}
                  theme="math"
                  onChange={this.handleChange} />
    )
  }
}

export default Create;
