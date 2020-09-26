import "@babel/polyfill";
import React from "react";
import ReactDOM from "react-dom";
import { HashRouter } from "react-router-dom";
import Main from "./components/Main";

const wrapper = document.getElementById("container");
wrapper
  ? ReactDOM.render(
      <HashRouter>
        <Main />
      </HashRouter>,
      wrapper
    )
  : false;
