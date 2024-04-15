import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import { ROOT, HOME } from "./constants";

export const RouterConfig = () => {
    return (
      <div>
        <Routes>
            <Route exact path={HOME} element={<Home/>} />
        </Routes>
      </div>
    );
  };