#include <DS3231.h>

int Relay = 4;

DS3231  rtc(SDA, SCL);
Time t;
//add after display;
const int OnHour = 07;
const int OnMin = 15;
const int OffHour = 07;
const int OffMin = 20;

void setup() {
  Serial.begin(115200);
  rtc.begin();
  pinMode(Relay, OUTPUT);
  digitalWrite(Relay, LOW);
  //rtc.setTime(21,10,00);//set your time and date by uncomenting these lines
  //rtc.setDate(26,6,2018);
}

void loop() {
  t = rtc.getTime();
  Serial.print(t.hour);
  Serial.print(" hour(s), ");
  Serial.print(t.min);
  Serial.print(" minute(s)");
  Serial.println(" ");
  delay (1000);
  
  if(t.hour == OnHour && t.min == OnMin){
    digitalWrite(Relay,HIGH);
    Serial.println("LIGHT ON");
    }
    
    else if(t.hour == OffHour && t.min == OffMin){
      digitalWrite(Relay,LOW);
      Serial.println("LIGHT OFF");
    }
}
