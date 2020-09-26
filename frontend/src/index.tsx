import "@babel/polyfill";
import React from "react";
import ReactDOM from "react-dom";
import { HashRouter } from "react-router-dom";
import Main from "./components/Main";

const wrapper = document.getElementById("container");
const basename = window.location.pathname.split("/").slice(0, -1).join("/");
wrapper
  ? ReactDOM.render(
      <HashRouter basename={basename}>
        <Main />
      </HashRouter>,
      wrapper
    )
  : false;
