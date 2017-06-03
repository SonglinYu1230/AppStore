var currentApp;

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
    for (var i = 0; i < apps.length; i++) {
        appendApp(apps[i]);
    }
}

function appendApp(app) {
    var relativeDiv = document.getElementById("middle-container");

    var rc = document.createElement("div");
    rc.setAttribute("class", "rectangle-container");

    var rcc = document.createElement("div");
    rcc.setAttribute("class", "rectangle");
    rc.appendChild(rcc);

    // var pType = ['app-name', 'download-page', 'version-info', 'package-info'];

    var textPrefix = ['应用名称:', 'BundleID:', '最新版本:', '平台类型:', '下载次数:'];
    var keys = ['name', 'id', 'version', 'app_platform', 'download_count'];
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

function uploadPlist(file) {
    var formData = new FormData();
    formData.append('platformType', 'iOS');
    formData.append('plist', file);

    uploadParsedInfo(formData, 'iOS');
}


function uploadMiniAPK(file, fileName) {
    var formData = new FormData();
    formData.append('platformType', 'Android');
    formData.append('fileName', fileName);
    formData.append('miniAPK', file);

    uploadParsedInfo(formData, 'Android');
}

function uploadParsedInfo(formData, platformtype) {
    var url = '/parseAppInfo';
    sendPostRequest(url, null, formData, function(xhr) {
        hideLoadingView();
        var jsonObject = JSON.parse(xhr.response);
        jsonObject['platformType'] = platformtype;
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
                if (result) {
                    uploadApp(jsonObject);
                }
            }
        });
    }, function(xhr) {});
}

function uploadApp(jsonObject) {
    var formData = new FormData();
    formData.append('platformType', jsonObject['platformType']);
    formData.append('appID', jsonObject['bundle_id']);
    formData.append('versionNumber', jsonObject['build_number']);
    formData.append('versionCode', jsonObject['version_number']);
    formData.append('appName', jsonObject['app_name']);
    formData.append('app', currentApp);

    showLoadingWithMessage();
    var url = '/uploadApp';
    sendPostRequest(url, null, formData, function(xhr) {
        var jsonObject = JSON.parse(xhr.response);
        jsonObject['id'] = jsonObject['app_id'];
        // var keys = ['name', 'id', 'version', 'app_platform', 'download_count'];
        appendApp(jsonObject);
        hideLoadingView();
        currentApp = '';
    }, function(xhr) {
        hideLoadingView();
        currentApp = '';
    });
}

function handleFiles(files) {
    showLoadingWithMessage();

    currentApp = files[0];
    var platformType = platformTypeWithFileName(currentApp.name);

    if (platformType === 'iOS') {
        handleIPA(currentApp);
    } else if (platformType === 'Android') {
        handleAPK(currentApp);
    } else {
        currentApp = '';
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