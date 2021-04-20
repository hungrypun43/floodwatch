#include <usbdrv.h>

#define SET_STATUS   0
#define GET_HEIGHT   1

////////////////////////////////////////////////////////////

#define RED_LED PIN_PC0
#define YELLOW_LED PIN_PC1
#define GREEN_LED PIN_PC2
const int pingPin = PIN_PC4;
int inPin = PIN_PC3;
////////////////////////////////////////////////////////////
usbMsgLen_t usbFunctionSetup(uint8_t data[8])
{
  usbRequest_t *rq = (usbRequest_t*)data;
  static uint8_t hcm ;//high in centemeter
  if(rq->bRequest == GET_HEIGHT){
    long cm = gotHeight();
    hcm = cm;
    usbMsgPtr = &hcm;
    return sizeof(hcm);
  }
  else if(rq->bRequest == SET_STATUS){
    uint8_t stat = rq->wValue.bytes[0];
    uint8_t stus = rq->wIndex.bytes[0];
    indicator(stat);
  }
  return 0;
}

///////////////////////////////////////////////////////////
long microsecondsToCentimeters(long microseconds)
{
  // ความเร็วเสียงในอากาศประมาณ 340 เมตร/วินาที หรือ 29 ไมโครวินาที/เซนติเมตร
  // ระยะทางที่ส่งเสียงออกไปจนเสียงสะท้อนกลับมาสามารถใช้หาระยะทางของวัตถุได้
  // เวลาที่ใช้คือ ระยะทางไปกลับ ดังนั้นระยะทางคือ ครึ่งหนึ่งของที่วัดได้
  return microseconds/58;
}

void indicator(uint8_t sta){
  if(sta==3){
    digitalWrite(RED_LED, HIGH);
  }
  else if(sta== 2){
    digitalWrite(YELLOW_LED, HIGH);
  }
  else if(sta = 1){
    digitalWrite(GREEN_LED, HIGH);
  }
  else{
    digitalWrite(RED_LED, HIGH);
    digitalWrite(YELLOW_LED, HIGH);
    digitalWrite(GREEN_LED, HIGH);
  }
}

void blackout(){
  digitalWrite(RED_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
}

long gotHeight(){
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
  return cm;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(RED_LED,OUTPUT);
  pinMode(YELLOW_LED,OUTPUT);
  pinMode(GREEN_LED,OUTPUT);
  usbInit();

  /* enforce re-enumeration of USB devices */
  usbDeviceDisconnect();
  delay(300);
  usbDeviceConnect();
}



void loop() {
  // put your main code here, to run repeatedly:
  usbPoll();
}
