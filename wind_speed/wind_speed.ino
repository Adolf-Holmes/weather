const int led=3;
void setup()
{
  pinMode(led,OUTPUT);
  Serial.begin(9600);     //使用9600的波特率进行串口通讯
}
void loop()
{

  int V1 = analogRead(A0);  //从A0口读取电压数据存入刚刚创建整数型变量V1，模拟口的电压测量范围为0-5V 返回的值为0-1024
  if (V1 < 2) V1 = 0;  //过滤杂波
  float vol = V1 * (5.0 / 1023.0);//我们将 V1的值换算成实际电压值存入浮点型变量 vol

  float wind_speed_km_h = 100.0 * vol;//电压值转换为风速值km/h
  float wind_speed_m_s = 27.8 * vol;//电压值转换为风速值m/s

  Serial.print(vol);                       //串口输出电压值，并且不换行
  Serial.print(" V    ");
  Serial.print(wind_speed_km_h);
  Serial.print(" km/h   ");
  Serial.print(wind_speed_m_s);
  Serial.print(" m/s");
  Serial.print(" \n");
  for(int i = 0;i < 255;i++)
  {
    analogWrite(led, i);
    delay(10);
  }
  for(int i = 255;i >= 0;i--)
  {
    analogWrite(led, i);
    delay(10);
  }
  delay(3000);                           //输出完成后等待0.1秒钟，用于控制数据的刷新速度。

}
