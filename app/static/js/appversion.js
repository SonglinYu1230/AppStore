function loadAppVersions(appID) {
    var formData = new FormData();
    formData.append('appID', appID);

    var url = "/appversion";
    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
        success: function(data, status, request) {
            // alert(data);
            if (data['isOk']) {
                str = JSON.stringify(data)
                alert(str);
            }
        },
    });
}

function getUrlVars() {
    var vars = [],
        hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}