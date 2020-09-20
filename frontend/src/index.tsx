import "@babel/polyfill";
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import Main from "./components/Main";

const wrapper = document.getElementById("container");
const basename = window.location.pathname.split("/").slice(0, -1).join("/");
wrapper
  ? ReactDOM.render(
      <BrowserRouter basename={basename}>
        <Main />
      </BrowserRouter>,
      wrapper
    )
  : false;
