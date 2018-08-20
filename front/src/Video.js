import React, { Component } from "react";
import PropTypes from "prop-types";
import Player from '@vimeo/player';
import "./Video.css";

const vids = [
  203857357,
  234703134,
  235561953,
  235562031,
  235562119,
];

// Component to play video
class Video extends Component {
  constructor(props) {
    super(props);

    this.state = {
      visible: false
    };

    this.onOpen = this.onOpen.bind(this);
    this.onClose = this.onClose.bind(this);
  }

  componentDidMount() {
    if (this.video) {
      this.player = new Player(this.video, {
          id: vids[this.props.currentStep],
          width: Math.floor(window.innerWidth * 0.45)
      });
    }
  }

  // Open pop up, play video
  onOpen() {
    this.setState({ visible: true });

    this.player.getVideoId().then((id) => {
      if (id !== vids[this.props.currentStep]) {
        this.player.loadVideo(vids[this.props.currentStep]).then(() => this.player.play());
      } else {
        this.player.play();
      }
    })
  }

  // Pause video, close pop up
  onClose() {
    this.player.pause();
    this.setState({ visible: false });
  }

  render() {
    return (
      <div>
        <button
          type="button"
          className="btn button1"
          onClick={this.onOpen}>
          Video hjelp
        </button>
        <div id="modal-video" className="modal" style={{ display: this.state.visible ? "block" : "none" }}>
          <div className="modal-contents">
            <span className="close" onClick={this.onClose}>&times;</span>
            <div ref={(ref) => this.video = ref} />
          </div>
        </div>
      </div>
    );
  }
}

Video.propTypes = {
  currentStep: PropTypes.number.isRequired
};

export default Video;
