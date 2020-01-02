#include <SoftwareSerial.h>
#include <string>
const int ledpin=13;
SoftwareSerial mySerial(10, 11);

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() {
    void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() {
   if (Serial.available()&&mySerial.available())
    {
      if('request' == Serial.read())
            CopeSerialData(mySerial.read());
            Serial.print(",");
            speed();
    }

}

char CopeSerialData(unsigned char ucData) {
  static unsigned char ucRxBuffer[250];
  static unsigned char ucRxCnt = 0;
  long  pmcf10 = 0;
  long  pmcf25 = 0;
  long  pmcf100 = 0;
  long  pmat10 = 0;
  long  pmat25 = 0;
  long  pmat100 = 0;
  long  pmcount03 = 0;
  long  pmcount05 = 0;
  long  pmcount10 = 0;
  long  pmcount25 = 0;
  long  pmcount50 = 0;
  long  pmcount100 = 0;
  ucRxBuffer[ucRxCnt++] = ucData;
  if (ucRxBuffer[0] != 0x42 && ucRxBuffer[1] != 0x4D) {
    ucRxCnt = 0;
    return ucRxCnt;
  }
  if (ucRxCnt < 32) {
    return ucRxCnt;
  }
  else {
    pmat25 = (float)ucRxBuffer[12] * 256 + (float)ucRxBuffer[13];  
    Serial.print("\"AqPM25:\""); 
    Serial.print(pmat25);
    ucRxCnt = 0;
    return ucRxCnt;
  }
}

int speed()
{
  int V1 = analogRead(A0);  //从A0口读取电压数据存入刚刚创建整数型变量V1，模拟口的电压测量范围为0-5V 返回的值为0-1024
  if (V1 < 2) V1 = 0;  //过滤杂波
  float vol = V1 * (5.0 / 1023.0);//我们将 V1的值换算成实际电压值存入浮点型变量 vol

  float wind_speed_km_h = 100.0 * vol;//电压值转换为风速值km/h
  float wind_speed_m_s = 27.8 * vol;//电压值转换为风速值m/s

  Serial.print("\"wind_speed:\"");
  Serial.print(wind_speed_km_h);
}