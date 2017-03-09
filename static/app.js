function myFunction() {
    var username = document.getElementById("username").value
    if (username.length < 6) {
        alert(document.getElementById("username").placeholder);
    }
}

function login() {
    $.post("http://0.0.0.0:5000/login", { "foo": "bar" })
        // window.location = 'http://127.0.0.1:5000/homepage.html'
        // return false
}