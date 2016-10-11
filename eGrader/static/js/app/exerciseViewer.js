import $ from 'jquery';
import {startMathJax, typesetMath} from "./mathjax.js";

window.$ = window.jQuery = $;

var App = {
  start() {
    startMathJax();
  },

  typeSetMath() {
    typesetMath(document);
  }

};

window.App = App;
