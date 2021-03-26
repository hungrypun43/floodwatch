#include <ESP8266WiFi.h>
#include <MicroGear.h>

const char* ssid     = "Your Wifi SSID";
const char* password = "Your Wifi Password";

#define APPID   "floodwatch"
#define KEY     "Tvimf2aifdM9sMu"
#define SECRET  "sQOnuhfP4ayrcX5N2M46nEvKe"

#define ALIAS   "Pod1"

#define Board_LED D0
#define RED_LED D3
#define YELLOW_LED D4
#define GREEN_LED D5
const int pingPin = D1;
int inPin = D2;

WiFiClient client;
MicroGear microgear(client);

unsigned long previousMillis = 0;
const long interval = 1000;
char data[32];


/* If a new message arrives, do this */
void onMsghandler(char *topic, uint8_t* msg, unsigned int msglen) {
  Serial.print("Incoming message --> ");
  msg[msglen] = '\0';
  Serial.println((char *)msg);
}

void onFoundgear(char *attribute, uint8_t* msg, unsigned int msglen) {
  Serial.print("Found new member --> ");
  for (int i = 0; i < msglen; i++)
    Serial.print((char)msg[i]);
  Serial.println();
}

void onLostgear(char *attribute, uint8_t* msg, unsigned int msglen) {
  Serial.print("Lost member --> ");
  for (int i = 0; i < msglen; i++)
    Serial.print((char)msg[i]);
  Serial.println();
}

void onConnected(char *attribute, uint8_t* msg, unsigned int msglen) {
  Serial.println("Connected to NETPIE...");
  microgear.setAlias(ALIAS);
}
long microsecondsToCentimeters(long microseconds)
{
  // ความเร็วเสียงในอากาศประมาณ 340 เมตร/วินาที หรือ 29 ไมโครวินาที/เซนติเมตร
  // ระยะทางที่ส่งเสียงออกไปจนเสียงสะท้อนกลับมาสามารถใช้หาระยะทางของวัตถุได้
  // เวลาที่ใช้คือ ระยะทางไปกลับ ดังนั้นระยะทางคือ ครึ่งหนึ่งของที่วัดได้
  return microseconds/58;
}
void indicator(long cm){
  if(cm<=20){
    digitalWrite(RED_LED, HIGH);
  }
  else if(cm<= 100){
    digitalWrite(YELLOW_LED, HIGH);
  }
  else{
    digitalWrite(GREEN_LED, HIGH);
  }
}

void blackout(){
  digitalWrite(RED_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
}

void setup() {

  microgear.on(MESSAGE, onMsghandler);
  microgear.on(PRESENT, onFoundgear);
  microgear.on(ABSENT, onLostgear);
  microgear.on(CONNECTED, onConnected);

  Serial.begin(115200);
  Serial.println("Starting...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }


  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  microgear.init(KEY, SECRET, ALIAS);
  microgear.connect(APPID);

  digitalWrite(2, HIGH);  //LED บนบอร์ด(GPIO 2)
  pinMode(2, OUTPUT);
  pinMode(Board_LED,OUTPUT);
  pinMode(RED_LED,OUTPUT);
  pinMode(YELLOW_LED,OUTPUT);
  pinMode(GREEN_LED,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  blackout();
  long duration, cm;
  if (microgear.connected()) {
    digitalWrite(2, LOW); //ไฟบนบอร์ดติดถ้าเชื่อมต่อ NETPIE
    microgear.loop();

    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) { //ทำงานทุกๆ 1 วินาที(interval)
      previousMillis = currentMillis;
      
      // put your main code here, to run repeatedly:
      
      
      pinMode(pingPin, OUTPUT);
      digitalWrite(pingPin, LOW);
      delayMicroseconds(2);
      digitalWrite(pingPin, HIGH);
      delayMicroseconds(5);
      digitalWrite(pingPin, LOW);
      pinMode(inPin, INPUT);
      duration = pulseIn(inPin, HIGH);
      cm = microsecondsToCentimeters(duration);
      indicator(cm);
      //Serial.print(cm);
      //Serial.print("cm");
      //Serial.println();
      //delay(1000);

      Serial.println("Publish...");

      sprintf(data, "%d", cm);   //แปรง int รวมกันใน char ชื่อ data
      Serial.println(data);
      microgear.publish("/x", data);      //ส่งค่าขึ้น NETPIE

//      microgear.publish("/x1", String(x1));     //หรือจะส่งทีละค่าก็ได้
//      microgear.publish("/x2", String(x2));
    }
  }
  else {
    digitalWrite(2, HIGH); //ไฟบนบอร์ดดับถ้าเชื่อมต่อ NETPIE ไม่ได้
    Serial.println("connection lost, reconnect...");
    microgear.connect(APPID);
  }
  delay(1000);
}
