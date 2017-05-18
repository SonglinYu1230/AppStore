function myFunction() {
    var username = document.getElementById("username").value
    if (username.length < 6) {
        alert(document.getElementById("username").placeholder);
    }
}

function session() {
    var url = "/session";
    var user = {
        'username': 'appupload',
        'password': '123456'
    }
    var http = new XMLHttpRequest();
    http.open("POST", url, true);
    http.setRequestHeader("Content-type", "application/json; charset=utf-8");
    // xmlhttp.setRequestHeader("Content-Type", "application/json");
    http.onreadystatechange = function() { //Call a function when the state changes.
        // if (http.readyState == 4 && http.status == 200) {
        //     // alert(http.responseText);
        //     // if (http.responseText["name"] === "Tom") {
        //     // window.location = "http://127.0.0.1:5000/homepage.html"
        // } else if (http.status == 302) {
        //     window.location = http.location;
        // }
        return false;
    }
    http.send(JSON.stringify(user));

}

function myChange() {
    oFiles = document.getElementById("file").files;
    f = oFiles[0];
    // f = extractPlist(f);
    uploadPlist(f);
}

function extractPlist(file) {
    var zip = new JSZip();
    zip.file("Hello.txt", "Hello World\n");
    var plist = zip.folder("images");
    img.file("smile.gif", imgData, { base64: true });
    zip.generateAsync({ type: "blob" })
        .then(function(content) {
            // see FileSaver.js
            saveAs(content, "example.zip");
        });
    return file
}

function uploadPlist(file) {
    var formData = new FormData();
    formData.append('username', 'johndoe');
    formData.append('id', 123456);
    formData.append('ipa', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://www.163.com/', true);
    xhr.onload = function(e) {
        console.log(e)
    };
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            alert(xhr.responseText);
        }
    }
    xhr.send(formData);
}

function uploadIpa(file) {
    var formData = new FormData();
    formData.append('username', 'johndoe');
    formData.append('id', 123456);
    formData.append('ipa', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/app/data', true);
    xhr.onload = function(e) {

    };
    xhr.send(formData);
}

function openapp() {
    // alert('excuse me');
    window.location = "weixin://1123"; //打开某手机上的某个app应用
    setTimeout(function() {
        window.location = 'https://www.google.com'; //如果超时就跳转到app下载页
    }, 500);
}