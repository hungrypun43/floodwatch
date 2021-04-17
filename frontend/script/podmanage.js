const URL = "http://localhost:5555";

function completeModal(name, podkey, secretKey) {
    document.getElementById("completePodname").innerText = "Pod Information for " + name;
    document.getElementById("completePodkey").value = podkey;
    document.getElementById("completeSecretkey").value = secretKey;
    //openModal();
    $('#completeModal').modal({
        show: true
      })
}
function copyClipboard(copyid) {
    var copyText = document.getElementById(copyid);
    copyText.select();
    copyText.setSelectionRange(0, 99999)
    document.execCommand("copy");
    alert("Copied the "+ copyid + " " + copyText.value);
}
function registerPod() {
    
    var nlatitude = document.getElementById("latitude").value;
    var nlongtitude = document.getElementById("longtitude").value;
    var npodname = document.getElementById("podname").value;
    var nsecretkey = document.getElementById("secretKey").value;
    var nharm = document.getElementById("harm").value;
    var naware = document.getElementById("aware").value;
    var nheight = document.getElementById("height").value;
    console.log(nlatitude);
    console.log(nlongtitude);
    console.log(npodname);
    console.log(nsecretkey);
    fetch(URL + "/addpods", {
        method: 'POST',
        body: JSON.stringify({
            podname: npodname,
            sheight: nheight,
            latitude: nlatitude,
            longtitude: nlongtitude,
            aware: naware,
            harm: nharm,
            podpassword: nsecretkey,
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
            },
        })
        .then((response) => response.json())
        .then((json) => completeModal(json["podname"], json["podkey"], json["secretkey"]));
}