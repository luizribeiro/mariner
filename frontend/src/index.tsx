import React from "react";
import ReactDOM from "react-dom";

import Main from "./components/Main.tsx";

const wrapper = document.getElementById("container");
wrapper ? ReactDOM.render(<Main />, wrapper) : false;
