// //Fetch Integration
// const getTodos = async () => {
// const options = {
// method: "GET",
// };
// const response = await fetch(
// "https://assets.breatheco.de/apis/fake/todos/user/keenerz",
// options
// );
// setList(await response.json());
// };

// useEffect(() => {
// getTodos();
// }, []);

// const saveTodoList = async (newTodos) => {
// console.log(newTodos);
// const options = {
// method: "PUT",
// body: JSON.stringify(newTodos),
// headers: { "content-type": "application/json" },
// };
// const response = await fetch(
// "https://assets.breatheco.de/apis/fake/todos/user/keenerz",
// options
// );
// console.log(JSON.stringify(newTodos.done));
// };
