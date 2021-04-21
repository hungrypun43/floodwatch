const URL = "http://localhost:5555" ; //your flask url

function open(publickey) {
    console.log("showstatus.html?openpod=" + publickey)
    //window.location.href = "showstatus.html?openpod=" + publickey;
}

function addpod(json) {
    console.log(json);
    console.log(json["podkey"])
    var command = "window.location.href =" + '"showstatus.html?openpod=' + json["podkey"]+ '";';
    console.log(command);
    document.getElementById("podstable").innerHTML = document.getElementById("podstable").innerHTML + "<tr onclick='"+ command +"'><th scope='row'>"+json["podname"]+"</th><td>"+status(json["podstatus"])+"</td>"
}
function status(st){
    if(st==3){
        return "🔴 รถเล็กไม่ควรผ่าน";
    }
    else if(st==2){
        return "🟡 ไม่ควรเดินเท้าผ่าน";
    }
    else if(st==1){
        return "🟢 สถานการณ์ปกติ";
    }
    else{
        return "ยังไม่มีการวัดค่า";
    }
}
function showallpod() {
    document.getElementById("podstable").innerHTML = document.getElementById("podstable").innerHTML + "</tbody></table>"
    fetch(URL)
        .then((response) => response.json())
        .then((json) => {
            console.log(json)
            json["data"].forEach(data => {
                addpod(data);
            });
        });
}

showallpod()