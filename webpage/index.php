<script src="https://cdn.netpie.io/microgear.js"></script>
<script src="js/raphael.2.1.0.min.js"></script>
<script src="js/justgage.1.0.1.min.js"></script>


<script>
	const APPKEY = "Tvimf2aifdM9sMu";
	const APPSECRET = "sQOnuhfP4ayrcX5N2M46nEvKe";
	const APPID = "floodwatch";

	var microgear = Microgear.create({
		gearkey: APPKEY,
		gearsecret: APPSECRET
	});

	var x=0,timestamp=0;

	microgear.on('message',function(topic,msg) {
		var split_msg = msg.split(",");
		var timestamp_current = new Date().getTime();
		console.log(split_msg);

		/*if(typeof(split_msg[3])=='undefined' || split_msg[3] == 'esp8266'){
				document.getElementById("esp8266").style.display = "block";
				document.getElementById("name").innerHTML = split_msg[3].toUpperCase();
				temp.refresh(split_msg[0]);
				humid.refresh(split_msg[1]);
				light.refresh(split_msg[2]);
				timestamp = timestamp_current;
		}
	});*/

	microgear.on('connected', function() {
		microgear.setname('webapp');
		document.getElementById("data").innerHTML = '<p><img src="img/nectec_logo.png" id="nectec" onclick="location.reload()"></p>';
	});

	setInterval(function(){
		var timestamp_current = new Date().getTime();

		if((timestamp_current-timestamp)>10000){
			document.getElementById("esp8266").style.display = "none";
		}
	},1000);

	microgear.resettoken(function(err){
		microgear.connect(APPID);
	});
</script>