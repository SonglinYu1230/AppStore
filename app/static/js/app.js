function myFunction() {
    var username = document.getElementById("username").value;
    if (username.length < 6) {
        alert(document.getElementById("username").placeholder);
    }
}

function session() {
    var url = "/session";
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var userInfo = {
        'username': user,
        'password': password
    };
    sendPostRequest(url, ContentTypeJSON, userInfo, null, function(xhr) {});
}

function myChange() {
    oFiles = document.getElementById("file").files;
    f = oFiles[0];
    // f = extractPlist(f);
    uploadIpa(f);
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
    return file;
}

function uploadPlist(files) {
    var formData = new FormData();
    formData.append('platformType', 'iOS');
    formData.append('plist', files[0]);

    var url = '/parseAppInfo';
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.onload = function(e) {
        alert(e);
    };
    xhr.send(formData);
}

function uploadAndroidFiles(files) {
    var formData = new FormData();
    formData.append('platformType', 'Android');
    formData.append('xml', files[0]);

    var url = '/parseAppInfo';
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.onload = function(e) {
        alert(e);
    };
    xhr.send(formData);
}


function uploadIpa(files) {
    var formData = new FormData();
    formData.append('platformType', 'iOS');
    formData.append('appID', 'com.app.test');
    formData.append('versionNumber', 333);
    formData.append('versionCode', '1.1.1');
    formData.append('appName', 'TestAPP');
    formData.append('app', files[0]);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/uploadApp', true);
    xhr.onload = function(e) {
        alert(e);
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