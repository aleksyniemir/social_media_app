
var sign_in_button = document.getElementById("login-button")

    sign_in_button.onclick = function() {
        let username = document.getElementById("username").value
        alert(username)
        let password = document.getElementById("password").value
        let url = "http:/127.0.0.1:8000/users/token"
        let xhr = new XMLHttpRequest()

        xhr.open("POST", url)
        xhr.setRequestHeader('Content-Type', 'application/json')

    }