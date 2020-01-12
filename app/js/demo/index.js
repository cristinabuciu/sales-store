$( document ).ready(function() {
    var cookie = $.cookie("username");
    if(cookie == null){
        window.location="login.html";
    } else {
        window.location="stock.html";
    }
    // $("#userStock").text(cookie);
    console.log( cookie );
});