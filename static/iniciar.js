
function addTask() {
  var taskInput = document.getElementById("taskInput");
  var taskList = document.getElementById("taskList");

  var newTask = document.createElement("li");
  newTask.innerHTML = taskInput.value;

  var deleteButton = document.createElement("button");
  deleteButton.innerHTML = "Deletar";
  deleteButton.addEventListener("click", function() {
    taskList.removeChild(newTask);
  });

  newTask.appendChild(deleteButton);
  taskList.appendChild(newTask);

  taskInput.value = "";
}