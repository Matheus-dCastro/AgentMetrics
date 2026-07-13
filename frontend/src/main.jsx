import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import Register from "./api/pages/Register";
import Login from "./api/pages/Login";
// import './index.css';

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    {/* <App /> */}
    {/* <Register /> */}
    <Login />
  </React.StrictMode>,
);
