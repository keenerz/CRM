import React, { useState, useEffect, useContext } from "react";
import { Context } from "../store/appContext.js";
import "../../styles/tasklist.css";

export const TaskList = () => {
  const { store, actions } = useContext(Context);
  let [task, setTask] = useState("");
  let [todotype, setTodotype] = useState("");
  let [stage, setStage] = useState("");
  let [acceptance, setAcceptance] = useState("");
  let [list, setList] = useState([]);

  // Input and mechanics
  const handleInput = (e) => {
    if (e.keyCode === 13 && e.target.value != "") {
      if (e.target.value.trim() === "") {
        alert("Error 404: words not found");
        setTask("");
      } else {
        setTask(e.target.value);
        setList([...list, { label: task, done: false }]);
        setTask("");
        saveTodoList([...list, { label: task, done: false }]);
      }
    }
  };

  return (
    <div className="d-inline justify-content-center w-100" id="whole">
      <div className="fw-light">
        <input
          className="form-control fw-light ps-5"
          id="inputZone"
          type="text"
          placeholder={
            list.length === 0
              ? "No tasks, add a task"
              : "What needs to be done?"
          }
          onChange={(event) => setTask(event.target.value)}
          onKeyDown={(e) => {
            handleInput(e);
          }}
          value={task}
        />
        <div className="selectors">
          <select
            className="feedback-input-selector"
            aria-label=""
            value={todotype}
            onChange={(e) => {
              setTodotype(e.target.value);
            }}
          >
            <option value="">Todo Type</option>
            <option value="bug/issue">Bug/Issue</option>
            <option value="feature">Feature</option>
            <option value="improvements">Improvements</option>
          </select>
          <select
            className="feedback-input-selector"
            aria-label=""
            value={stage}
            onChange={(e) => {
              setStage(e.target.value);
            }}
          >
            <option value="">Stage</option>
            <option value="notdone">Not Done</option>
            <option value="inprogress">In Progress</option>
            <option value="done">Done</option>
          </select>
          <select
            className="feedback-input-selector"
            aria-label=""
            value={acceptance}
            onChange={(e) => {
              setAcceptance(e.target.value);
            }}
          >
            <option value="">Acceptance</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
            <option value="furtherreview">Further Review Needed</option>
          </select>
        </div>
      </div>
      <div id="list">
        <ul>
          {list.map((singleTask, i) => {
            return (
              <li
                className={`d-flex justify-content-between ps-5 py-2 text-muted fw-light fs-5 ${
                  singleTask.done ? "done" : ""
                }`}
                key={i}
              >
                {singleTask.label}{" "}
                <div className="theButtons">
                  <div
                    className="listDone"
                    onClick={() => {
                      let newList = [...list];
                      newList[i].done = !newList[i].done;
                      setList(newList);
                      saveTodoList(newList);
                    }}
                  >
                    <i className="fas fa-check"></i>
                  </div>
                  <div
                    className="listDelete"
                    onClick={() => {
                      setList(list.filter((deleteTask, j) => j !== i));
                      saveTodoList(list.filter((deleteTask, j) => j !== i));
                    }}
                  >
                    <i className="fas fa-trash"></i>
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
        <div className="ps-3 py-2 fw-light text-start" id="footer">
          <span id="footerText">
            {list.length} {list.length === 1 ? "item" : "items"} left
          </span>
        </div>
      </div>
    </div>
  );
};
