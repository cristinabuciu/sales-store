function logout() {
    var username =$.cookie("username");
    $.removeCookie("username");
    $.removeCookie("token");
    $.removeCookie("scope");

    $.ajax({
        // url: "http://192.168.99.124:5001/logout",
        url: "http://localhost:5001/logout",
        type: "POST",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        data: JSON.stringify({
            "username":username
        }),
        // contentType: "application/json",
        cache: false
    }).done(function (result) {
        console.log("done");
        var jsonResult = JSON.parse(result);
        console.log(jsonResult)
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
// needs to implement if it fails
    });

    window.location="login.html";


}