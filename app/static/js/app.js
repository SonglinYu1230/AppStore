function myFunction() {
    var username = document.getElementById("username").value;
    if (username.length < 6) {
        alert(document.getElementById("username").placeholder);
    }
}

function login() {
    var url = "/login";
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var userInfo = {
        'username': username,
        'password': password
    };
    // sendPostRequest(url, ContentTypeJSON, userInfo, function(xhr) {

    // }, function(xhr) {});

    $.ajax({
        type: 'POST',
        url: url,
        data: userInfo,
        success: function(data) { alert('data: ' + data); },
    });
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

function uploadMiniAPK(file, fileName) {
    var formData = new FormData();
    formData.append('platformType', 'Android');
    formData.append('fileName', fileName);
    formData.append('miniAPK', file);

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

function handleFile(files) {
    var fullPath = document.getElementById('file2').value;
    var platformType = platformTypeWithFilePath(fullPath);
    if (platformType === 'iOS') {
        alert(platformType);
    } else if (platformType === 'Android') {
        handleAPK(files[0]);
    } else {}
}

function platformTypeWithFilePath(fullPath) {
    var re = /(?:\.([^.]+))?$/;
    var fileExtension = re.exec(fullPath)[1].toUpperCase();
    if (fileExtension === 'IPA') {
        return 'iOS'
    } else if (fileExtension === 'APK') {
        return 'Android';
    } else {
        return '';
    }
}

function handleAPK(file) {
    var new_zip = new JSZip();
    new_zip.loadAsync(file).then(function(zip) {
            var uploadZip = new JSZip();
            zip.filter(function(relativePath, f) {
                if (relativePath === 'AndroidManifest.xml' || relativePath === 'resources.arsc') {
                    uploadZip.file(f.name, f._data);
                }
            });
            uploadZip.folder('res');
            uploadZip.filter(function(relativePath, f) {
                console.log(relativePath);
            });
            uploadZip.generateAsync({
                type: "blob",
                compression: "DEFLATE"
            }).then(function(content) {
                uploadMiniAPK(content, file.name);
            });
        },
        function(e) {

        });
}

function openapp() {
    window.location = "weixin://1123"; //打开某手机上的某个app应用
    setTimeout(function() {
        window.location = 'https://www.google.com'; //如果超时就跳转到app下载页
    }, 500);
}