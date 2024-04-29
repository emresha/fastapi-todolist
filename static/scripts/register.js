function userRegister(event) {
    event.preventDefault()
    var userUsername = document.getElementById("username_reg").value;
    var userPassword = document.getElementById("password_reg").value;

    var data = {
        "login": userUsername,
        "password": userPassword
    };

    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");

            }
            return response.json()
        })
        .then(data => {
            console.log("Register successful!")
        })
        .catch(error => {
            console.error("Error registering: ", error)
        })

}