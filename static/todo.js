const todolist = document.querySelector(".todolist");

show(); 

function update(data) {
	tasklist = data['tasks']
	var html = "";
	if (tasklist.length) {
		tasklist.forEach((task, idx) => {
			html += `<li> ${task} <span><button class= "button-todo" onclick = "delete_task(${idx})"><i class="fas fa-trash"></i></button></span></li>`
		})
	}
	todolist.innerHTML = html;
}

function show() {
	fetch(`${window.origin}/getdata`, {
		method : "POST",
		headers: new Headers({
			"content-type" : "application/json"
		})
	}).then(function(response) {
		response.json().then(function(data) {
			update(data);
		});
	});
}

function add_task() {
	var user_input = document.getElementById("todo_input").value;

	var entry = {
		task: user_input
	};
	fetch(`${window.origin}/add`, {
		method : "POST",
		body: JSON.stringify(entry),
		headers: new Headers({
			"content-type" : "application/json"
		})
	}).then(function(response) {
		response.json().then(function(data) {
			update(data);
		});
	});
}

function delete_task(id) {
	var page = 0;
	if (window.location.href == `${window.origin}/work`) {
		page = 1;
	}
	var entry = {
		task_id: id,
		page: page
	};
	fetch(`${window.origin}/delete`, {
		method : "POST",
		body: JSON.stringify(entry),
		headers: new Headers({
			"content-type" : "application/json"
		})
	}).then(function(response) {
		response.json().then(function(data) {
			update(data);
		});
	});
}	