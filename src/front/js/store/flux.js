const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      todos: [],
    },
    actions: {
      //Login and Token items
      getCurrentSession: () => {
        const session = JSON.parse(localStorage.getItem("session"));
        return session;
      },
      login: async (email, password) => {
        const store = getStore();
        const actions = getActions();
        const options = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        };

        try {
          const response = await fetch(
            process.env.BACKEND_URL + `/api/token`,
            options
          );
          if (response.status !== 200) {
            alert("Incorrect Email or Password");
            return false;
          }

          const data = await response.json();
          localStorage.setItem("session", JSON.stringify(data));
          setStore({ session: data });
          actions.loadTodos();
          return true;
        } catch (error) {
          console.error("Error in login zone");
        }
      },
      logout: () => {
        const store = getStore();
        const actions = getActions();
        localStorage.removeItem("session");
        setStore({ session: null });
        localStorage.removeItem("useredit");
        setStore({ useredit: null });
        actions.loadProjects();
      },
      //Todo Functions
      loadTodos: async () => {
        const store = getStore();
        const actions = getActions();
        const session = actions.getCurrentSession();
        let options = {
          headers: {
            Authorization: "Bearer " + session?.token,
          },
        };
        if (!session) {
          options.headers = {};
        }
        const response = await fetch(
          process.env.BACKEND_URL + `/api/todos`,
          options
        );
        if (response.status === 200) {
          const payload = await response.json();
          setStore({ projects: payload });
        }
      },
      saveTodoList: async (newTodos) => {
        const actions = getActions();
        const session = actions.getCurrentSession();
        const options = {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + session.token,
          },
          body: JSON.stringify({
            todos: newTodos.todos,
            todo_type: newTodos.todo_type,
            stage: newTodos.stage,
            acceptance: newTodos.acceptance,
            due_date: newTodos.due_date,
            details: newTodos.details,
          }),
        };
        const response = await fetch(
          process.env.BACKEND_URL + `/api/todos`,
          options
        );
        if (response.status === 200) {
          const payload = await response.json();
          console.log("project created successfully!");
          actions.loadProjects();
          return payload;
        }
      },
    },
  };
};

export default getState;
