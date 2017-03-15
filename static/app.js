function myFunction() {
    var username = document.getElementById("username").value
    if (username.length < 6) {
        alert(document.getElementById("username").placeholder);
    }
}

function login() {
    var http = new XMLHttpRequest();
    var url = "http://0.0.0.0:5000/login";
    http.open("POST", url, true);
    //Send the proper header information along with the request
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    http.onreadystatechange = function() { //Call a function when the state changes.
        if (http.readyState == 4 && http.status == 200) {
            // alert(http.responseText);
            // if (http.responseText["name"] === "Tom") {
            // window.location = "http://127.0.0.1:5000/homepage.html"
        }
    }
    http.send("fname=Bill&lname=Gates");
}

function myChange() {
    oFiles = document.getElementById("file").files;
    f = oFiles[0];

    var formData = new FormData();
    formData.append('username', 'johndoe');
    formData.append('id', 123456);
    formData.append('ipa', f);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/app/data', true);
    xhr.onload = function(e) {

    };
    xhr.send(formData);
    return;


    alert(oFiles[0].size);
    // 上传文件
    // var url = "http://0.0.0.0:5000/app/data";

    var formData = new FormData();
    // formData.append('section', 'general');
    // formData.append('action', 'previewImg');
    // Main magic with files here
    formData.append('ipa', f);

    $.ajax({
        url: 'http://0.0.0.0:5000/app/data',
        type: 'POST',
        data: formData,
        contentType: 'multipart/form-data',
        // THIS MUST BE DONE FOR FILE UPLOADING
        processData: false,
        success: function (data) {
            jsonData = JSON.parse(data);
            alert(data);
        }
    });
}