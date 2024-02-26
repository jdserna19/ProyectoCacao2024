//Arduino 2

//MANIFEST//
/*
   Flow Rate (L/min)
   Wind Speed (m/s)
   Solenoid Valve (0 = close, 1 = Open)
   Rotatory Arm angle (0° - 360°)
*/
//Variable time definitions
unsigned long tcurrent = 0;
unsigned long tinitial = 0;
long time_samp = 1000; //Sampling time 1 sec for sensors
float WVALSTATE;

//Motor PIN DEFINITION
int DIR = 23;
int STEP = 9;
int VEL = 130;
int t = 10;
/*Position of the top arm*/
//int nov = 1050;
int nov = 1300;
//int hf = 3150;
int hf = 3200;
//int comp = 4200;
int comp = 4700;
/*Current angle*/
float act_angle = 0;
float angle = 0;

//WIND SPEED SENSOR (m/s)//
/* Variables */
char  databuffer[35];
double  temp;
String val;

//SOLENOID VALVE//
#define solenoidPin 8

// FLOW RATE Variables//
#define flowPin 2 //The pin location of the sensor
volatile int NbTopsFan; //measuring the rising edges of the signal
float Calc;
const int num_reads = 10;
int reads_fw[num_reads] = {0}; int read_index_fw = 0; long total_fw = 0; double fw_read_smth = 0; double fl_smth = 0;

/* Functions for Flow Rate */
//1   Reading RPM
void rpm ()     //This is the function that the interupt calls
{
  NbTopsFan++;  //This function measures the rising and falling edge of the hall effect sensors signal
}

//2   L/min calculation
void l_min()
{
  NbTopsFan = 0;   //Set NbTops to 0 ready for calculations
  sei();      //Enables interrupts
  tinitial = millis();
  while ((millis() - tinitial) <= time_samp) {}                                 //Wait 1 second
  cli();      //Disable interrupts
  Calc = (NbTopsFan * 60); //(Pulse frequency x 60) / Q, = flow rate in L/hour  //L/min readings w/out SMOOTH
  fl_smth = smooth_ot(Calc , total_fw, reads_fw, read_index_fw);
  sei();
}

//Function Digital or other sensors for the taken measurements
unsigned long smooth_ot(float &data, long &total, int *readings, int &readIndex)
{
  // subtract the last reading
  total = total - readings[readIndex];
  // read from the sensor:
  readings[readIndex] = data;
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;
  // if we're at the end of the array...
  if (readIndex >= num_reads)
  { // ...wrap around to the beginning:
    readIndex = 0;
  }
  // calculate the average:
  return total / num_reads;
}

/* Functions for Wind Sensor */
//1
void getBuffer()//Get weather status data
{
  int index;
  for (index = 0; index < 35; index ++)
  {
    if (Serial1.available())
    {
      databuffer[index] = Serial1.read();
      if (databuffer[0] != 'c')
      {
        index = -1;
      }
    }
    else
    {
      index --;
    }
  }
}
//2
int transCharToInt(char *_buffer, int _start, int _stop) //char to int
{
  int _index;
  int result = 0;
  int num = _stop - _start + 1;
  int _temp[num];
  for (_index = _start; _index <= _stop; _index ++)
  {
    _temp[_index - _start] = _buffer[_index] - '0';
    result = 10 * result + _temp[_index - _start];
  }
  return result;
}
//Wind Direction
int WindDirection()
{
  return transCharToInt(databuffer, 1, 3);
}
//air Speed (1 minute)
float WindSpeedAverage()
{
  temp = 0.44704 * transCharToInt(databuffer, 5, 7);
  return temp;
}
//Max air speed (5 minutes)
float WindSpeedMax()
{
  temp = 0.44704 * transCharToInt(databuffer, 9, 11);
  return temp;
}
//Temperature ("C")
float Temperature()
{
  temp = (transCharToInt(databuffer, 13, 15) - 32.00) * 5.00 / 9.00;
  return temp;
}
//Rainfall (1 hour)
float RainfallOneHour()
{
  temp = transCharToInt(databuffer, 17, 19) * 25.40 * 0.01;
  return temp;
}
//Rainfall (24 hours)
float RainfallOneDay()
{
  temp = transCharToInt(databuffer, 21, 23) * 25.40 * 0.01;
  return temp;
}
//Humidity
int Humidity()
{
  return transCharToInt(databuffer, 25, 26);
}
//Barometric Pressure
float BarPressure()
{
  temp = transCharToInt(databuffer, 28, 32);
  return temp / 10.00;
}

/* Functions for POLOLU MOTOR */
//////////////////////////
///From others LOT's to L1
void D1(int c)
{
  //From L2 to L1
  if (c == 2)
  {
    for (int i = 0; i <= nov; i++)
    {
      digitalWrite(DIR, LOW);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 1;
    //Serial.println(act_angle);
  }
  //From L4 to L1
  else if (c == 4)
  {
    for (int i = 0; i <= comp; i++)
    {
      digitalWrite(DIR, LOW);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 1;
  }
  //From L3 to L1
  else if (c == 3)
  {
    for (int i = 0; i <= hf; i++)
    {
      digitalWrite(DIR, LOW);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 1;
  }
}

//////////////////////////
///From others LOT's to L2
void D2(int c)
{
  //From L1 to L2
  if (c == 1)
  {
    for (int i = 0; i <= nov; i++)
    {
      digitalWrite(DIR, HIGH);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 2;
  }
  //From L3 to L2
  else if (c == 3)
  {
    for (int i = 0; i <= 2000; i++)
    {
      digitalWrite(DIR, LOW);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 2;
  }
  //From L4 to L2
  else if (c == 4)
  {
    for (int i = 0; i <= hf; i++)
    {
      digitalWrite(DIR, LOW);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 2;
  }
}
/////////////////////////////////////
///From others LOT's to L3
void D3(int c)
{
  //From L2 to L3
  if (c == 2)
  {
    for (int i = 0; i <= 2000; i++)
    {
      digitalWrite(DIR, HIGH);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 3;
  }
  //From L4 to L3
  else if (c == 4)
  {
    for (int i = 0; i <= nov; i++)
    {
      digitalWrite(DIR, LOW);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 3;
  }
  //From L1 to L3
  else if (c == 1)
  {
    for (int i = 0; i <= hf; i++)
    {
      digitalWrite(DIR, HIGH);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 3;
  }
}
/////////////////////////////////////
///From others LOT's to L4
void D4(int c)
{
  //From L3 to L4
  if (c == 3)
  {
    for (int i = 0; i <= nov; i++)
    {
      digitalWrite(DIR, HIGH);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 4;
  }
  //From L1 to L4
  else if (c == 1)
  {
    for (int i = 0; i <= comp; i++)
    {
      digitalWrite(DIR, HIGH);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 4;
  }
  //From L2 to L4
  else if (c == 2)
  {
    for (int i = 0; i <= hf; i++)
    {
      digitalWrite(DIR, LOW);
      analogWrite(STEP, VEL);
      delay(t);
    }
    analogWrite(STEP, 0);
    act_angle = 4;
  }
}
/////////////////////////////////////
void ch_angle(int b)
{
  if (b == 1)
  {
    angle = 45;
  }
  else if (b == 2)
  {
    angle = 135;
  }
  else if (b == 3)
  {
    angle = 225;
  }
  else if (b == 4)
  {
    angle = 315;
  }
}


void setup() {
  Serial.begin(9600);
  Serial1.begin(9600); //Wind speed sensor
  pinMode(DIR, OUTPUT);
  Serial.println("Ready");
  pinMode(flowPin, INPUT); //initializes digital pin 2 as an input
  attachInterrupt(0, rpm, RISING); //and the interrupt is attached
  WVALSTATE = 0;
  act_angle = 1;
}

void loop() {
  getBuffer();//Begin!
  RainfallOneHour();
  RainfallOneDay();
  Temperature();
  Humidity();
  WindSpeedMax();
  WindDirection();
  //l_min();
  if (Serial.available() > 0)
  {
    val = Serial.readStringUntil('\n');
    if (val.equals("GD"))
    {
      Serial.println(fl_smth, DEC); //Flow in L/min
      Serial.println(WindSpeedAverage()); //Wind speed average for 1 min
      Serial.println(WVALSTATE);
      Serial.println(angle);
    }
    else if (val.equals("RAL1"))
    {
      D1(act_angle);
      ch_angle(act_angle);
      Serial.println(angle);
    }
    else if (val.equals("RAL2"))
    {
      //Serial.println("entro");
      D2(act_angle);
      ch_angle(act_angle);
      Serial.println(angle);
    }
    else if (val.equals("RAL3"))
    {
      D3(act_angle);
      ch_angle(act_angle);
      Serial.println(angle);
    }
    else if (val.equals("RAL4"))
    {
      D4(act_angle);
      ch_angle(act_angle);
      Serial.println(angle);
    }
    else if (val.equals("RB"))
    {
      digitalWrite(solenoidPin, HIGH);
      WVALSTATE = 1;
      Serial.println(WVALSTATE);
    }
    else if (val.equals("RE"))
    {
      digitalWrite(solenoidPin, LOW);
      WVALSTATE = 0;
      Serial.println(WVALSTATE);
    }
  }
}
