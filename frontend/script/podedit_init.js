const URL = "http://localhost:5555" ; //your flask url

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

function value_Init(json) {
    document.getElementById("headlabel").innerText = "Edit the " + json["podname"];
    document.getElementById("latitude").value = json["podlatitude"];
    document.getElementById("longtitude").value = json["podlongtitude"];
    document.getElementById("podname").value = json["podname"];
    document.getElementById("height").value = json["podsetupheight"];
    document.getElementById("aware").value = json["podaware"];
    document.getElementById("harm").value = json["podharm"];
}

function gotmyData(token) {
    fetch(URL + "/mydata", {method: "GET",
        headers:{
            'x-access-token' : token,
        },
    }).then((response) => response.json())
    .then((json) => value_Init(json));
}

function editPod() {
    
    var nlatitude = document.getElementById("latitude").value;
    var nlongtitude = document.getElementById("longtitude").value;
    var npodname = document.getElementById("podname").value;
    var nharm = document.getElementById("harm").value;
    var naware = document.getElementById("aware").value;
    var nheight = document.getElementById("height").value;
    console.log(nlatitude);
    console.log(nlongtitude);
    console.log(npodname);
    fetch(URL + "/mydata", {
        method: 'PUT',
        body: JSON.stringify({
            podname: npodname,
            setuph: Number(nheight),
            latitude: Number(nlatitude),
            longtitude: Number(nlongtitude),
            aware: Number(naware),
            harm: Number(nharm),
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'x-access-token' : token,
            },
        })
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
            alert("Update successful!!");
            location.reload();
        });
}

var token= getCookie("token");
console.log(token);
if(!token){
    window.location.href = "./loginaspodeditor.html";
}
else{
    gotmyData(token);
}