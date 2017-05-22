var ContentTypeJSON = 'JSON';

function sendPostRequest(url, contentType, params, successCallback, failureCallback) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status >= 200 && xhr.status < 300 || xhr.status == 302) {
                console.log(response);
                alert(xhr.responseText);
                if (successCallback) {
                    successCallback();
                }
            } else {
                // alert("Request was unsuccessful" + xhr.status);
                alert(xhr.response)
                if (failureCallback) {
                    failureCallback(xhr);
                }
            }
        }
    }
    if (contentType === ContentTypeJSON) {
        xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");
        params = JSON.stringify(params);
    }
    xhr.send(params);
}