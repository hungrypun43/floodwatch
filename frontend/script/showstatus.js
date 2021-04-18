const FlaskURL = "http://localhost:5555";
var status = 1;
var gauge3 = Gauge(
    document.getElementById("gauge3"),
    {
      max: 100,
      value: 10,
      color: function() {
        if(status==1){
            return "#26fc84 ";
        }
        else if(status==2){
            return "#fc9b26";
        }
        else if(status==3){
            return "#fc2626";
        }
        else{
            return "#581845";
        }
      }
    }
  );

function fillStatus(json) {
    document.getElementById("podname").innerText = json["podname"];
    gauge3.setValue(json["podheight"]);
    status = json["podstatus"];
    if(json["podstatus"]==1){
        document.getElementById("status").innerText = "ปลอดภัยในการเดินเท้า";
    }
    else if(json["podstatus"]==2){
        document.getElementById("status").innerText = "ไม่แนะนำให้เดินเท้า";
    }
    else if(json["podstatus"]==3){
        document.getElementById("status").innerText = "ไม่แนะนำให้รถยนต์ผ่าน";
    }
    else{
        document.getElementById("status").innerText = "ไม่ระบุ";
    }
}

function init_status(public_key) {
    fetch(FlaskURL + "/getpoddata/" + public_key)
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
            fillStatus(json);
            
        });
}


function getUrlVars() {
    var vars = {}
    var parts = window.location.href.replace(
      /[?&]+([^=&]+)=([^&]*)/gi,
      function (m, key, value) {
        vars[key] = value
      }
    )
    return vars
  }
  
function getUrlParam(parameter, defaultvalue) {
    var urlparameter = defaultvalue
    if (window.location.href.indexOf(parameter) > -1) {
      urlparameter = getUrlVars()[parameter]
    }
    return urlparameter
}

function init_fetch(podkey){
    fetch(FlaskURL + "/getpoddata/" + podkey)
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
            fillStatus(json);
            console.log(Number(json["podlatitude"]))
            var mymap = L.map('mapid').setView([Number(json["podlatitude"]), Number(json["podlongtitude"])], 13);

            L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=LNrIlBZrMfpFPgZQeM7m', {
            attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    
            }).addTo(mymap);
            var marker = L.marker([Number(json["podlatitude"]), Number(json["podlongtitude"])]).addTo(mymap);
        });
}

var podkey = getUrlParam("openpod");

console.log(podkey);
init_fetch(podkey);
setInterval(init_status, 5000, podkey);

