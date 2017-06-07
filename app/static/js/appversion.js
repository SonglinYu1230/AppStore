function loadAppVersions(appID) {
    var formData = new FormData();
    formData.append('appID', appID);

    var url = "/appversion";
    sendPostRequest(url, null, formData, function(xhr) {
        var jsonObject = JSON.parse(xhr.response);
        if (jsonObject['isOK']) {
            var apps = jsonObject['apps'];
            insertApps(apps);
        }
    }, function(xhr) {});
}

function insertApps(apps) {
    for (var i = 0; i < apps.length; i++) {
        appendApp(apps[i]);
    }
}

function appendApp(app) {
    var relativeDiv = document.getElementById("container");
    var btn = document.createElement("BUTTON");
    btn.onclick = downloadApp;
    btn.attributes['app'] = app;
    str = '点击下载' + app['app_id'];
    var t = document.createTextNode(str);
    btn.appendChild(t);
    relativeDiv.appendChild(btn);
}

function downloadApp() {
    var app = this.attributes['app'];
    console.log(app);

    var url = "/download/app";
    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(app),
        success: function(data) {
            console.log(data);
            if (data.redirect) {
                window.location = data.redirect;
            }
        },
        contentType: 'application/json',
        dataType: 'json',
    });

}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}