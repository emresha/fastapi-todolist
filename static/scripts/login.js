    document.getElementById("loginForm").addEventListener("submit", function(event) {
        event.preventDefault();

        var formData = new FormData(this);
        var username = document.getElementById("username").value;
        var password = document.getElementById("password").value;

        var request = new XMLHttpRequest();
        request.open("PUT", "/login");

        request.setRequestHeader("login", username);
        request.setRequestHeader("password", password);

        request.send(new URLSearchParams(formData));

        request.onload = function() {
            if (request.status >= 200 && request.status < 300) {
                console.log("Login successful");
                console.log(request.responseText);
                window.location.reload(); // Refresh the page
            } else {
                console.error("Login failed");
                console.error(request.responseText);
            }
        };
    });