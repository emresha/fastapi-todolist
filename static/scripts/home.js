// Function to generate HTML block for todo
function generateTodoHTML(todo) {
    return `
        <div class="todo-item">
            <h2>${todo.title}</h2>
            <p>Status: ${todo.status === 0 ? 'Incomplete' : 'Complete'}</p>
            <p>Description: ${todo.description}</p>
            <p>Owner: ${todo.owner}</p>
            <p>Creation Date: ${todo.creation_date ? todo.creation_date : 'N/A'}</p>
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

// Call fetchTasksAndRender to fetch tasks and render them
fetchTasksAndRender();