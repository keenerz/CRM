import React, { useState, useEffect } from "react";

const TaskList = () => {
  let [task, setTask] = useState("");
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

  //Fetch Integration
  const getTodos = async () => {
    const options = {
      method: "GET",
    };
    const response = await fetch(
      "https://assets.breatheco.de/apis/fake/todos/user/keenerz",
      options
    );
    setList(await response.json());
  };

  useEffect(() => {
    getTodos();
  }, []);

  const saveTodoList = async (newTodos) => {
    console.log(newTodos);
    const options = {
      method: "PUT",
      body: JSON.stringify(newTodos),
      headers: { "content-type": "application/json" },
    };
    const response = await fetch(
      "https://assets.breatheco.de/apis/fake/todos/user/keenerz",
      options
    );
    console.log(JSON.stringify(newTodos.done));
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
export default TaskList;
