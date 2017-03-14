function myFunction() {
    var username = document.getElementById("username").value
    if (username.length < 6) {
        alert(document.getElementById("username").placeholder);
    }
}

function login() {
    // $.post("http://0.0.0.0:5000/login", { "foo": "bar" })
    // window.location = 'http://127.0.0.1:5000/homepage.html'
    // return false
    var http = new XMLHttpRequest();
    var url = "http://0.0.0.0:5000/login";
    var params = "lorem=ipsum&name=binny";
    http.open("POST", url, true);

    //Send the proper header information along with the request
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    http.onreadystatechange = function() { //Call a function when the state changes.
        if (http.readyState == 4 && http.status == 200) {
            alert(http.responseText);
            // if (http.responseText["name"] === "Tom") {
            // window.location = "http://127.0.0.1:5000/homepage.html"
        }
    }
    http.send(params);
}
}

function uploadFile() {
    // window.location = 'homepage.html'
    // $('#file-input').trigger('click');
    return false
}

// $(function() {
//     $('#file').bind('change', function() {
//         var f = this.files[0]
//             // alert(f.size);
//             // alert(f.name);
//             // alert(f.mimetype);
//         var formData = new FormData();
//         formData.append('file', f);

//         $.ajax({
//             url: 'upload.php',
//             type: 'POST',
//             data: formData,
//             processData: false, // tell jQuery not to process the data
//             contentType: false, // tell jQuery not to set contentType
//             success: function(data) {
//                 console.log(data);
//                 alert(data);
//             }
//         });
//     })
// })