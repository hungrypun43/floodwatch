#define Board_LED D0
#define RED_LED D3
#define YELLOW_LED D4
#define GREEN_LED D5
const int pingPin = D1;
int inPin = D2;

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
  // put your setup code here, to run once:
  pinMode(Board_LED,OUTPUT);
  pinMode(RED_LED,OUTPUT);
  pinMode(YELLOW_LED,OUTPUT);
  pinMode(GREEN_LED,OUTPUT);
  Serial.begin(9600);
  
  
  
}

void loop() {
  // put your main code here, to run repeatedly:
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
  indicator(cm);
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();
  delay(1000);
}
