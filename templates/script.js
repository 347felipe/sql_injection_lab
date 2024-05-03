document.getElementById("btn").addEventListener("click", sendLoginInfo);

function sendLoginInfo() {
    var username = document.getElementById("username").value;
    var pass = document.getElementById("pass").value;
    fetch("http://localhost:5000/login", {
        method: "POST",
        redirect: "follow",
        body: JSON.stringify({
            username: username,
            password: pass,
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            console.error("Login failed");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}