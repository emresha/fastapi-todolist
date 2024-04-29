function logOut(event) {
    fetch("/logout", {
        method: "PUT",
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");

            }
            return response.json()
        })
        .then(data => {
            console.log("Logout successful!")
            location.reload()
        })
        .catch(error => {
            console.error("Error logout: ", error)
        })
}