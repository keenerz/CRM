import React, { useState } from "react";
import { TaskList } from "../component/tasklist";

export const Home = () => {
  return (
    <div className="container-flex">
      <div className="row px-5 d-flex justify-content-center" id="outerTask">
        <div
          className="text-center d-flex justify-content-center"
          id="innerTask"
        >
          <TaskList />
        </div>
      </div>
    </div>
  );
};
