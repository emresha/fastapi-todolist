function markAsDone(event) {
    event.preventDefault();

    var todoItem = event.target.closest(".todo-item");

    var taskId = todoItem.dataset.id;

    var data = {
        id: taskId
    };

    // send a PUT request to the endpoint with the JSON data
    fetch('/complete_task', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Handle successful response
        console.log('Task marked as done successfully.');
        location.reload();
    })
    .catch(error => {
        // Handle error
        console.error('There was a problem marking the task as done:', error);
    });
}
