const URL = "http://localhost:5555" ; //your flask url

var mylat, mylong;
console.log("hello");
var x = document.getElementById("mapid");
var mymap;
function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showMap);
      navigator.geolocation.getCurrentPosition(gotdata);
    } else {
      x.innerHTML = "Geolocation is not supported by this browser.";
    }
  }
function showMap(position){
    //console.log(position.coords.latitude);
    mylat = position.coords.latitude;
    mylong = position.coords.longitude;
    mymap = L.map('mapid').setView([position.coords.latitude, position.coords.longitude], 13);

    L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=LNrIlBZrMfpFPgZQeM7m', {
    attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    }).addTo(mymap);
}

function openD(podkey) {
  window.location.href = "./showstatus.html?openpod=" + podkey;
}
function distance(lat1, lon1, lat2, lon2, unit) {
  var radlat1 = Math.PI * lat1/180
  var radlat2 = Math.PI * lat2/180
  var theta = lon1-lon2
  var radtheta = Math.PI * theta/180
  var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
  if (dist > 1) {
      dist = 1;
  }
  dist = Math.acos(dist)
  dist = dist * 180/Math.PI
  dist = dist * 60 * 1.1515
  if (unit=="K") { dist = dist * 1.609344 }
  if (unit=="N") { dist = dist * 0.8684 }
  return dist
}

function findnearest(data,position) {
  var min = -1;
  var keymin;
  data.forEach(dat =>{
    console.log(dat["podlatitude"]);
    console.log(dat["podlongtitude"]);
    //console.log(position.coords.latitude);
    var d = distance(position.coords.latitude, position.coords.longitude, Number(dat["podlatitude"]), Number(dat["podlongtitude"]), "K");
    console.log(d);
    if(min==-1){
      min = d;
      keymin = dat["podkey"];
    }
    else if(d<min){
      min = d;
      keymin = dat["podkey"];
    }
    
  })
  openD(keymin);
}
function gotdata(position) {
  fetch(URL)
  .then((response) => response.json())
  .then((json) => {
      findnearest(json["data"], position);
  });
}
getLocation();
//gotdata();