#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>

#define Board_LED D0
#define RED_LED D3
#define YELLOW_LED D4
#define GREEN_LED D5
const int pingPin = D1;
int inPin = D2;


String servername = "yourflasklink/uppod/";
String podkey = "podkey";
String secretkey = "secretkey";



void indicator(String level){
  if(level== "3"){
    digitalWrite(RED_LED, HIGH);
  }
  else if(level== "2"){
    digitalWrite(YELLOW_LED, HIGH);
  }
  else if(level== "1"){
    digitalWrite(GREEN_LED, HIGH);
  }
  else{
    digitalWrite(RED_LED, HIGH);
    digitalWrite(YELLOW_LED, HIGH);
    digitalWrite(GREEN_LED, HIGH);
  }
}

long microsecondsToCentimeters(long microseconds)
{
  // ความเร็วเสียงในอากาศประมาณ 340 เมตร/วินาที หรือ 29 ไมโครวินาที/เซนติเมตร
  // ระยะทางที่ส่งเสียงออกไปจนเสียงสะท้อนกลับมาสามารถใช้หาระยะทางของวัตถุได้
  // เวลาที่ใช้คือ ระยะทางไปกลับ ดังนั้นระยะทางคือ ครึ่งหนึ่งของที่วัดได้
  return microseconds/58;
}

void blackout(){
  digitalWrite(RED_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
}

void setup () {
  pinMode(Board_LED,OUTPUT);
  pinMode(RED_LED,OUTPUT);
  pinMode(YELLOW_LED,OUTPUT);
  pinMode(GREEN_LED,OUTPUT);
  Serial.begin(115200);
  WiFi.begin("thamdeena 2.4G", "thamadee");
 
  while (WiFi.status() != WL_CONNECTED) {
 
    delay(1000);
    Serial.println("Connecting..");
 
  }
  Serial.println("Connected to WiFi Network");
 
}
 
void loop() {
  blackout();
  long duration, cm;
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);
  pinMode(inPin, INPUT);
  duration = pulseIn(inPin, HIGH);
  cm = microsecondsToCentimeters(duration);
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
    
    HTTPClient http;  //Declare an object of class HTTPClient
    String hlink = servername + podkey;
    http.begin(hlink); //Specify request destination
    http.addHeader("Content-Type", "application/json");
    String mycm = String(cm); 
    String wrd = "{\"secretkey\": \"" + secretkey + "\", \"height\":" + mycm + "}";
    int httpCode = http.PUT(wrd); //Send the request
 
    if (httpCode > 0) { //Check the returning code
 
      String payload = http.getString();   //Get the request response payload
      Serial.println(payload); //Print the response payload
      indicator(payload);
 
    }else Serial.println("An error ocurred");
 
    http.end();   //Close connection
 
  }
 
  delay(10000);    //Send a request every 10 seconds
 
}
