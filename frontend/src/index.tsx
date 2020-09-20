import "@babel/polyfill";
import React from "react";
import ReactDOM from "react-dom";
import Main from "./components/Main";

const wrapper = document.getElementById("container");
wrapper ? ReactDOM.render(<Main />, wrapper) : false;
