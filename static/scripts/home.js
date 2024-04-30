// function to generate HTML block for todo
function generateTodoHTML(todo) {
    return `
        <div class="todo-item" data-id="${todo.id}">
            <h2>${todo.title}</h2>
            ${todo.status === 0 ? '<p class="Incomplete">Incomplete</p>' : '<p class="Complete">Complete</p>'}</p>
            <p>${todo.description}</p>
            <p>Creation Date: ${todo.creation_date ? todo.creation_date : 'N/A'}</p>
            ${todo.status === 0 ? '<button class="done-button" onclick=\"changeTask(event, 1)\"><img src=\"./static/img/done.svg\" height="32" alt=\"Mark As Done\"/>Mark As Done</button>' : ""}
            ${todo.status === 1 ? '<button class="undone-button" onclick=\"changeTask(event, 0)\"><img src=\"./static/img/cross.png\" height="32" alt=\"Mark As Undone\"/>Mark As Undone</button>' : ""}
        </div>
    `;
}

// function to fetch data from the server and extract tasks from headers
async function fetchTasksAndRender() {
    try {
        const response = await fetch('/');
        const tasksHeader = response.headers.get('tasks');
        if (!tasksHeader) {
            console.error('Tasks header not found in response');
            return;
        }
        const jsonData = JSON.parse(tasksHeader);

        var todoHTML = '';
        jsonData.forEach(function(todo) {
            todoHTML += generateTodoHTML(todo);
        });

        // append generated HTML to the todoList section
        document.getElementById('todoList').innerHTML = todoHTML;
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

fetchTasksAndRender();