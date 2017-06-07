function loadApps() {
    var url = "/apps";
    $.ajax({
        type: 'POST',
        url: url,
        data: null,
        success: function(data, status, request) {
            // alert(data);
            if (data['isOK']) {
                str = JSON.stringify(data)
                alert(str);
            }
        },
    });
}