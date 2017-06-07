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
            if (data['isOK']) {
                window.location.href = '/home';
            }
        },
    });
}