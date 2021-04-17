const URL = "http://localhost:5555";

function authenticateUser(podkey, secretKey)
{
    var token = podkey + ":" + secretKey;

    // Should i be encoding this value????? does it matter???
    // Base64 Encoding -> btoa
    var hash = btoa(token); 

    return "Basic " + hash;
}

function gotToken(podkey, secretkey) {
    var auth = authenticateUser(podkey, secretkey);
    fetch(URL + "/auth", {method: "GET",
        headers: {
            'Authorization': auth,
        },
    }).then((response) => response.json())
    .then((json) => {
        console.log(json);
        if (json["token"]!= undefined) {
            keepCookie(json["token"]);
        }
        else{
            alert("Pod " + json["message"]);
            console.log(json["message"]);
        }
    }
    );
}

function keepCookie(token) {
    var d = new Date();
    d.setTime(d.getTime() + (60*60*1000));
    var expires = "expires" + d.toGMTString();
    document.cookie = "token=" + token + ";" + expires + ";path=/";
    //checkCookie("token");
    window.location.href = "./editpod.html";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
  }

function checkCookie() {
    var user= getCookie("token");
    if (user != "") {
      alert("Welcome again " + user);
    } else {
       user = prompt("Please enter your name:","");
       if (user != "" && user != null) {
         setCookie("username", user, 30);
       }
    }
  }
function gotuserParameter() {
    var podkey = document.getElementById("podkey").value;
    var secretKey = document.getElementById("secretKey").value;
    console.log(podkey);
    console.log(secretKey);
    gotToken(podkey, secretKey);
}
