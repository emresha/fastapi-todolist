document.getElementById("create-task").addEventListener("click", function() {
    var overlay = document.createElement("div");
    overlay.style.position = "fixed";
    overlay.style.top = "0";
    overlay.style.left = "0";
    overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    overlay.style.zIndex = "9999";
    document.body.appendChild(overlay);
    var popup = document.createElement("div");
    popup.id = "popupOverlay";
    popup.style.position = "fixed";
    popup.style.top = "50%";
    popup.style.left = "50%";
    popup.style.transform = "translate(-50%, -50%)";
    popup.style.zIndex = "10000";
    document.body.appendChild(popup);

    var headerTask = document.createElement("h2");
    headerTask.textContent = "New Task";
    popup.appendChild(headerTask);

    var titleInput = document.createElement("input");
    titleInput.type = "text";
    titleInput.placeholder = "Title";
    titleInput.style.display = "block";
    titleInput.style.marginBottom = "10px";
    popup.appendChild(titleInput);

    var descriptionInput = document.createElement("textarea");
    descriptionInput.type = "text";
    descriptionInput.placeholder = "Description";
    descriptionInput.style.display = "block";
    descriptionInput.style.marginBottom = "10px";
    popup.appendChild(descriptionInput);

    var addButton = document.createElement("button");
    addButton.textContent = "Add";
    addButton.style.display = "block";
    addButton.style.marginTop = "10px";
    addButton.addEventListener("click", function() {
        console.log("Title:", titleInput.value);
        console.log("Description:", descriptionInput.value);

        var data = {
            "title": titleInput.value,
            "description": descriptionInput.value
        }

        fetch("/create_task", {
            method: "POST",
            headers: {
            "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response error")
                }
                return response.json()
            })
            .then(data => {
                console.log("Successfully added task")
                location.reload()
            })
            .catch(error => {
                console.error("Error adding task")
                location.reload()
            });

        document.body.removeChild(popup);
        document.body.removeChild(overlay);
    });
    popup.appendChild(addButton);

    // Close button
    var closeButton = document.createElement("button");
    closeButton.textContent = "Close";
    closeButton.style.display = "block";
    closeButton.style.marginTop = "10px";
    closeButton.addEventListener("click", function() {
        // Close the popup window
        document.body.removeChild(popup);
        document.body.removeChild(overlay);
    });
    popup.appendChild(closeButton);
});