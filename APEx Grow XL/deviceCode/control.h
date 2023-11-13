#include "config.h"
#include "pinMap.h"

class PIDController
{
public:
  PIDController(int targ, int p, int i, int d);
  PIDController();
  float updateOutput(float newVal);
  void setCoeffs(float p, float i, float d);
  void resetIntegral();
  void setTarget(float targ);

  void applyClipping(float overSat);

private:
  float target;

  float error;
  float prevError;
  float runningIntegral;

  float a;

  float kp;
  float ki;
  float kd;

  unsigned long prevMillis;
};

class TempController
{
public:
  TempController(float targ, int outputPin_);
  TempController(float targ, int outputPin_, boolean reversed_);
  void updateOutput(float newVal);
  void setTarget(float targ);
  void setModePID(float p, float i, float d);
  void setModeHyst(float lb, float ub);
  void setModeOnOff();

  byte heaterPower;
  byte heaterPowerSet;

  PIDController pid;
  int controlMode;
  float target;
  void setHeaterPower();

private:
  int outputPin;
  boolean reversed;

  unsigned long cycleStartTime;
  unsigned int heaterDutyCycle = 30;

  //  PIDController pid;
  //  int controlMode;
  //  int target;

  int lowerHystVal;
  int upperHystVal;

  unsigned long prevMillis;
};

//class PumpController
//{
//public:
//  byte pump1Speed = 0;
//  byte pump2Speed = 0;
//  byte pump3Speed = 0;
//  byte pump4Speed = 0;
//  byte pump5Speed = 0;
//  byte fanSpeed = 0;
//
//  boolean pump1Dir = false;
//  boolean pump2Dir = false;
//  boolean pump3Dir = false;
//  boolean pump4Dir = false;
//  boolean pump5Dir = false;
//  boolean fanDir = false;
//
//  boolean pump1Overide = false;
//  boolean pump2Overide = false;
//  boolean pump3Overide = false;
//  boolean pump4Overide = false;
//  boolean pump5Overide = false;
//  boolean fanOveride = false;
//
//  unsigned long dilutionTime = 1000;
//  unsigned long dilutionStartTime = 0;
//  boolean dilutionFlag = false;
//  byte dilutionPower = 0;
//  byte maxDilutionPower = 255;
//
//  boolean fixedDilutionRateEnabled = false;
//  unsigned long fixedDilutionRate = 10000;
//
//  PumpController();
//  byte setPump1(byte power, boolean dir);
//  byte setPump2(byte power, boolean dir);
//  byte setPump3(byte power, boolean dir);
//  byte setPump4(byte power, boolean dir);
//  byte setPump5(byte power, boolean dir);
//  byte setFan(byte power);
//
//  void dilute(byte power);
//  void updatePumps();
//
//private:
//  byte setPump(byte power, boolean dir, int spdPin, int onOffPin, int dirPin);
//};

class ODController
{
public:
  ODController(float targ);
  void updateOutput(float newVal);
  void setTarget(float targ);
  void setTarget(float targ, float drift);
  void setModePID(float p, float i, float d);
  void setModeHyst(float lb, float ub);
  void setModeOnOff();
  void setModeConstFlow(int power);

  byte pumpPower;
  int safetyFactor = 2;

  int controlMode;
  float target;

private:
  void setPumps();

  PIDController pid;

  float lowerHystVal = 0;
  float upperHystVal = 0;

  unsigned long prevMillis;
};


class PumpController2
{
public:
  PumpController2();

  boolean speedsChanged = false;
  
  int speedPins[totalPumps] = {pump1SpeedPin, pump2SpeedPin, pump3SpeedPin,
                      pump4SpeedPin, pump5SpeedPin, pump6SpeedPin,
                      pump7SpeedPin,fanSpeedPin,fan2SpeedPin};
                      
  int dirPins[totalPumps] = {pump1DirPin, pump2DirPin, pump3DirPin,
                      pump4DirPin, pump5DirPin, pump6DirPin,
                      pump7DirPin,dudPin,dudPin};

  boolean reversible[totalPumps] = {true,true,true,true,true,true,true,false,false};
  boolean twoPinReverse[totalPumps] = {true,false,false,true,false,false,false,false,false};

  int onOffPins[totalPumps] = {pump1DirPin2, pump2OnOffPin, pump3OnOffPin,
                      pump4DirPin2, pump5OnOffPin, pump6OnOffPin,
                      pump7OnOffPin,dudPin,dudPin};   // for the DC motors instead of this being an enable pin its instead the second direction pin



  int pumpSpeeds[totalPumps] = {0,0,0,0,0,0,0,0,0};
  boolean pumpOverides[totalPumps] = {false,false,false,false,false,false,false,false,false};
  unsigned long pumpOffTime = [0,0,0,0,0,0,0,0,0]; // holds the time that the pumps should turn off at (0 is ignored)
  int nonOverideSpeeds[totalPumps] = {0,0,0,0,0,0,0,0,0};

  int mediaPrepSetup = 2;  // 0 nothing connected, 1 media bottle in place, 2 heated media, 3 media maker 

  void applySpeedToPump(int pumpNum);
  
  void setPumpSpeed(int pumpNum, int pumpSpeed, boolean overide);

  void releasePumpOverides(int pumpNum, boolean overide);

  void dilute(int power);

  void cycleSensors();
  
  void updatePumps();

  unsigned long pumpUpdateTime = 0;
  unsigned long latest_time = 0;

  unsigned long dilutionTime = 4000;
  unsigned long dilutionStartTime = 0;
  unsigned long dilutionEndTime = 0;
  signed long excessTimeNeeded = 0;
  boolean dilutionFlag = false;
  int dilutionStage = 0;
  byte dilutionPower = 0;
  byte maxDilutionPower = 255;

  boolean fixedDilutionRateEnabled = false;
  unsigned long fixedDilutionRate = 10000;

private:

  float accrewedDilutionVolume[3] = {0.0,0.0,0.0};  //{Media In, Media Transfer, Waste}

  float volumeOffsetThreshold = 0.2;
  
  float pumpFullFlowRate[4] = {21.125,21.7917,21.70833,12.0};    // {Media In, Media Transfer, Waste, Sterilization}
  float pump2sFlowRate[4] = {17.625,17.91666667,17.75,12.0};
  float pump4sFlowRate[4] = {19,19.75,19.51666667,12.0};
  float pump6sFlowRate[4] = {19.41666667,20.375,20.08333333,12.0};  
};
