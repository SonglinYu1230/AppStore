var loadingView;

function signin() {
    var url = "/login";
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var userInfo = {
        'username': username,
        'password': password
    };
    // sendPostRequest(url, null, userInfo, function(xhr) {

    // }, function(xhr) {});

    $.ajax({
        type: 'POST',
        url: url,
        data: userInfo,
        success: function(data, status, request) {
            if (data['isOk']) {
                window.location.href = '/home';
            }
        },
    });
}

function loadApps() {
    var url = "/apps";
    $.ajax({
        type: 'POST',
        url: url,
        data: null,
        success: function(data, status, request) {
            // alert(data);
            if (data['isOk']) {
                insertApps(data['apps']);
            }
        },
    });
}

function insertApps(apps) {
    Array.prototype.push.apply(apps, apps);
    Array.prototype.push.apply(apps, apps);

    var relativeDiv = document.getElementById("middle-container");
    for (var i = 0; i < apps.length; i++) {
        var rc = document.createElement("div");
        rc.setAttribute("class", "rectangle-container");

        var rcc = document.createElement("div");
        rcc.setAttribute("class", "rectangle");
        rc.appendChild(rcc);

        // var pType = ['app-name', 'download-page', 'version-info', 'package-info'];

        var textPrefix = ['应用名称:', 'BundleID:', '最新版本:', '平台类型:', '下载次数:'];
        var keys = ['name', 'id', 'version', 'app_platform', 'download_count'];
        var app = apps[i];
        for (var j = 0; j < textPrefix.length; j++) {
            var para = document.createElement('P');
            // para.setAttribute("class", pType[j]);
            rcc.appendChild(para);

            var str = textPrefix[j] + app[keys[j]];
            var t = document.createTextNode(str);
            rcc.appendChild(t);
        }

        var para = document.createElement("P");
        rcc.appendChild(para);

        var buttonNames = ['编辑', '预览', '删除'];
        for (var m = 0; m < buttonNames.length; m++) {
            var btn = document.createElement("BUTTON");
            var t = document.createTextNode(buttonNames[m]);
            btn.appendChild(t);
            rcc.appendChild(btn);
        }

        relativeDiv.appendChild(rc);
    }
}

function uploadPlist(file) {
    var formData = new FormData();
    formData.append('platformType', 'iOS');
    formData.append('plist', file);

    var url = '/parseAppInfo';
    sendPostRequest(url, null, formData, function(xhr) {
        hideLoadingView();

        bootbox.confirm({
            title: "App信息",
            message: xhr.response,
            // className: 'bb-alternate-modal',
            buttons: {
                cancel: {
                    label: '<i class="fa fa-times"></i> 取消'
                },
                confirm: {
                    label: '<i class="fa fa-check"></i> 上传'
                }
            },
            callback: function(result) {
                console.log('This was logged in the callback: ' + result);
            }
        });
    }, function(xhr) {});

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
        hideLoadingView();
        bootbox.alert({
            message: "This is an alert with an additional class!",
            className: 'bb-alternate-modal'
        });
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

function handleFiles(files) {
    loadingView = showLoadingWithMessage();

    var file = files[0];
    var platformType = platformTypeWithFileName(file.name);

    if (platformType === 'iOS') {
        handleIPA(file);
    } else if (platformType === 'Android') {
        handleAPK(file);
    } else {
        hideLoadingView();
    }
}

function platformTypeWithFileName(fielName) {
    var re = /(?:\.([^.]+))?$/;
    var fileExtension = re.exec(fielName)[1].toUpperCase();
    if (fileExtension === 'IPA') {
        return 'iOS'
    } else if (fileExtension === 'APK') {
        return 'Android';
    } else {
        return '';
    }
}

function handleIPA(file) {
    var new_zip = new JSZip();
    new_zip.loadAsync(file).then(function(zip) {
            var plists = zip.file(/Payload\/[^/]+.app\/Info.plist/);
            if (plists.length > 0) {
                var plist = plists[0];
                console.log(plist);
                var uploadZip = new JSZip();
                uploadZip.file('Info.plist', plist._data);
                uploadZip.generateAsync({
                    type: "blob",
                    compression: "DEFLATE"
                }).then(function(content) {
                    uploadPlist(content, 'Info.plist');
                });
            }
        },
        function(e) {

        });
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

// alert
function showLoadingWithMessage() {
    return bootbox.dialog({
        message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>'
    })
}

function hideLoadingView() {
    loadingView.modal('hide');
}