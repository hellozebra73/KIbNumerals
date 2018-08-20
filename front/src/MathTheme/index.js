import SnowTheme from "quill/themes/snow";
import { BaseTooltip } from "quill/themes/base";
import katex from "katex";
import MathQuill from "mathquill";
import extend from "extend";
import "./index.css";

// Get MathQuill instance
const MQ = MathQuill.getInterface(2);

// Export Katex so Quill can find it
window.katex = katex;

class MathTheme extends SnowTheme {
  extendToolbar(toolbar) {
    super.extendToolbar(toolbar);
    this.mathTooltip = new MathTooltip(this.quill, this.options.bounds);
  }
}

// Change default behaviour for formulas
MathTheme.DEFAULTS = extend(true, {}, SnowTheme.DEFAULTS, {
  modules: {
    toolbar: {
      handlers: {
        formula: function(value) {
          this.quill.theme.mathTooltip.edit('formula');
        },
      }
    }
  }
});


class MathTooltip extends BaseTooltip {
  constructor(quill, bounds) {
    super(quill, bounds);
    const tooltip = this;
    const formula = this.root.querySelector('.ql-formula');

    // Create quill
    this.mathInput = MQ.MathField(formula, {
      spaceBehavesLikeTab: true,
      handlers: {
        edit: function() {
          tooltip.textbox.value = tooltip.mathInput.latex();
        }
      }
    });

    formula.addEventListener("keyup", (event) => {
      if (event.which === 13) {
        event.preventDefault();
        this.save();
      } else if (event.keyCode === 27) {
        this.hide();
      }
    });
  }

  listen() {
    super.listen();

    this.root.querySelector('a.ql-action').addEventListener('click', event => {
      this.save();
      event.preventDefault();
    });
  }

  edit(mode = 'link', preview = null) {
    super.edit(mode, preview);
    this.mathInput.focus();
  }

  hide() {
    if (this.mathInput) {
      this.mathInput.latex("");
      this.textbox.value = "";
    }

    super.hide();
  }
}

MathTooltip.TEMPLATE = [
 '<input style="display:none" type="text" data-formula="a=1/2" data-link="https://quilljs.com" data-video="Embed URL">',
 '<div class="ql-formula"></div>',
 '<a class="ql-action"></a>',
].join('');

export { MathTooltip, MathTheme as default };
