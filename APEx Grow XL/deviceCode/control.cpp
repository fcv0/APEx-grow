#include "control.h"

//generic PID controller
PIDController::PIDController(int targ, int p, int i, int d) {
  setCoeffs(p, i, d);
  setTarget(targ);
  prevError = 0;
}

PIDController::PIDController() {
  setCoeffs(0, 0, 0);
  setTarget(0);
  prevError = 0;
  prevMillis = millis();
}

float PIDController::updateOutput(float newVal) {
  float elapsedTime = (millis() - prevMillis) / 1000;

  error = target - newVal;
  runningIntegral += ((error + prevError) / 2) * elapsedTime;
  a = (kp * error + ki * runningIntegral + kd * ((error - prevError) / elapsedTime));

  prevError = error;
  prevMillis = millis();
  return a;
}

void PIDController::setCoeffs(float p, float i, float d) {
  kp = p;
  ki = i;
  kd = d;
}

void PIDController::resetIntegral() {
  runningIntegral = 0;
}

void PIDController::setTarget(float targ) {
  target = targ;
}

void PIDController::applyClipping(float overSat){
  runningIntegral += -overSat/ki;
}


//Temperature controller
TempController::TempController(float targ, int outputPin_) {
  reversed = false;
  outputPin = outputPin_;
  target = targ;
  controlMode = 1;
  pid = PIDController(targ, 0, 0, 0);
  cycleStartTime = millis();
  heaterPower = 0;
  heaterPowerSet = 0;
}

TempController::TempController(float targ, int outputPin_, bool reversed_) {
  reversed = reversed_;
  target = targ;
  controlMode = 1;
  pid = PIDController(targ, 0, 0, 0);
  cycleStartTime = millis();
  heaterPower = 0;
  heaterPowerSet = 0;
}

void TempController::updateOutput(float newVal) {
  if (controlMode == 1) {            //on off
    if (newVal < target) {
      heaterPower =  255;
    } else {
      heaterPower =  0;
    }
  } else if (controlMode == 2) {      //hysteressis
    if (newVal < lowerHystVal) {
      heaterPower = 255;
    } else if (newVal > upperHystVal) {
      heaterPower = 0;
    }
  } else if (controlMode == 3) {      //pid
    float pidOut =  pid.updateOutput(newVal);
    heaterPower = (int) min(255, max(0, pidOut));
    float overSaturation = 0;
    if (pidOut > 255.0){
      overSaturation = pidOut - 255.0;
    }else if (pidOut < 0){
      overSaturation = pidOut;
    }
    pid.applyClipping(overSaturation);
  } else {
    heaterPower = 0;
  }
  if(reversed){
    heaterPower = 255 - heaterPower;
  }
  setHeaterPower();
}
void TempController::setTarget(float targ) {
  target = targ;
  if (controlMode == 3) {
    pid.setTarget(target);
  }
}
void TempController::setModePID(float p, float i, float d) {
  if (controlMode == 3) {
    pid.setCoeffs(p, i, d);
  } else {
    controlMode = 3;
    pid = PIDController(target, p, i, d);
  }
}

void TempController::setModeHyst(float lb, float ub) {
  if (controlMode == 2) {
    lowerHystVal = lb;
    upperHystVal = ub;
  } else {
    controlMode = 2;
    lowerHystVal = lb;
    upperHystVal = ub;
  }
}

void TempController::setModeOnOff() {
  controlMode = 1;
}

void TempController::setHeaterPower() {
  if (heaterPower > 255) {
    heaterPower = 255;
  } else if (heaterPower < 0) {
    heaterPower = 0;
  }
  unsigned long curTime = millis();
  unsigned long cycleTime = curTime - cycleStartTime;
  if (cycleTime > heaterDutyCycle * 1000) {
    cycleStartTime += heaterDutyCycle * 1000;
    cycleTime = curTime - cycleStartTime;
  }
  unsigned long triggerTime = ((unsigned long)heaterDutyCycle * 1000 * (unsigned long)heaterPower);
  if (255 * cycleTime < triggerTime) {
    digitalWrite(outputPin, HIGH);
    heaterPowerSet = 255;
  } else {
    digitalWrite(outputPin, LOW);
    heaterPowerSet = 0;
  }
}

//OD control
ODController::ODController(float targ) {
  target = targ;
  controlMode = 1;
  pid = PIDController(targ, 0, 0, 0);
  pumpPower = 0;
}

void ODController::updateOutput(float newVal) {   ///target is an OD
  if (controlMode == 1) {            //on off
    if (newVal < target) {
      pumpPower =  0;
    } else {
      pumpPower =  255;
    }
  } else if (controlMode == 2) {      //hysteressis
    if (newVal < lowerHystVal){
      pumpPower = 0;
    }else if(newVal < upperHystVal){
      pumpPower = pumpPower;
    }else if(newVal > upperHystVal){
      pumpPower = 255;
    }
  } else if (controlMode == 4) {      //pid
    float pidOut =  pid.updateOutput(newVal);
    pumpPower = (int) min(255, max(0, pidOut));
  } else {
    pumpPower = 0;
  }
  setPumps();
}
void ODController::setTarget(float targ) {
  target = targ;
  if (controlMode == 4) {
    pid.setTarget(target);
  }
  if (controlMode == 2) {
    controlMode = 1;
  }
}

void ODController::setTarget(float targ, float drift) {
  target = targ;
  if(drift == 0){
    controlMode = 1;
  }else{
    controlMode = 2;
    upperHystVal = target + abs(drift);
    lowerHystVal = target - abs(drift);
  }
}

void ODController::setModePID(float p, float i, float d) {
  if (controlMode == 4) {
    pid.setCoeffs(p, i, d);
  } else {
    controlMode = 4;
    pid = PIDController(target, p, i, d);
  }
}

void ODController::setModeHyst(float lb, float ub) {
  if (controlMode == 2) {
    lowerHystVal = lb;
    upperHystVal = ub;
  } else {
    controlMode = 2;
    lowerHystVal = lb;
    upperHystVal = ub;
  }
}

void ODController::setModeOnOff() {
  controlMode = 1;
}

void ODController::setModeConstFlow(int power) {
  controlMode = 0;
  pumpPower = power;
}

void ODController::setPumps() {
  if (pumpPower > 255) {
    pumpPower = 255;
  } else if (pumpPower < 0) {
    pumpPower = 0;
  }
}


//Pump Control functions
//PumpController::PumpController() {
//  dilutionStartTime = millis();
//}
//
//byte PumpController::setPump(byte power, boolean dir, int spdPin, int onOffPin, int dirPin) {
//  if (power == 0) {
//    analogWrite(spdPin, 0);
//    delay(20);
//    digitalWrite(onOffPin, LOW);
//  }
//  else {
//    analogWrite(spdPin, power);
//    digitalWrite(onOffPin, HIGH);
//  }
//  digitalWrite(dirPin, !dir);
//  return power;
//}
//
//byte PumpController::setPump1(byte power, boolean dir) {
//  if (!pump1Overide){
//    pump1Speed = power;
//    pump1Dir = dir;
//  }
//  return setPump(pump1Speed,pump1Dir, pump1SpeedPin, pump1DirPin2, pump1DirPin);
//}
//
//
//byte PumpController::setPump2(byte power, boolean dir) {
//  if (!pump2Overide){
//    pump2Speed = power;
//    pump2Dir = dir;
//  }
//  return setPump(pump2Speed,pump2Dir, pump2SpeedPin, pump2OnOffPin, pump2DirPin);
//}
//
//
//byte PumpController::setPump3(byte power, boolean dir) {
//  if (!pump3Overide){
//    pump3Speed = power;
//    pump3Dir = dir;
//  }
//  return setPump(pump3Speed,pump3Dir, pump3SpeedPin, pump3OnOffPin, pump3DirPin);
//}
//
//
//byte PumpController::setPump4(byte power, boolean dir) {
//  if (!pump4Overide){
//    pump4Speed = power;
//    pump4Dir = dir;
//  }
//  return setPump(pump4Speed,pump4Dir, pump4SpeedPin, pump4DirPin2, pump4DirPin);
//}
//
//
//byte PumpController::setPump5(byte power, boolean dir) {
//  if (!pump5Overide){
//    pump5Speed = power;
//    pump5Dir = dir;
//  }
//  return setPump(pump5Speed,pump5Dir, pump5SpeedPin, pump5OnOffPin, pump5DirPin);
//}
//
//byte PumpController::setFan(byte power) {
//  if (!fanOveride){
//    fanSpeed = power;
//  }
//  return setPump(fanSpeed, false, fanSpeedPin, fanOnOffPin, dudPin);
//}
//
//void PumpController::dilute(byte power) {
//  float workingValue = float(power) * float(maxDilutionPower)/255.0;
//  dilutionPower = (byte) round(workingValue);
//  dilutionFlag = true;
//  dilutionStartTime = millis();
//  setPump3(dilutionPower, false);
//}
//
//void PumpController::updatePumps() {
//  if (dilutionFlag) {
//    if (millis() - dilutionStartTime > 2 * dilutionTime) {
//      dilutionFlag = false;
//      setPump3(0, false);
//      setPump5(0, false);
//    } else if (millis() - dilutionStartTime > dilutionTime) {
//      setPump3(0, false);
//      setPump5(dilutionPower, false);
//    }
//  }else if (fixedDilutionRateEnabled){
//    if ((millis() - dilutionStartTime) > fixedDilutionRate){
//      dilute(255);
//    }
//  }
//}

PumpController2::PumpController2(){
  
}

void PumpController2::applySpeedToPump(int pumpNum){
  
  analogWrite(speedPins[pumpNum], abs(pumpSpeeds[pumpNum]));

  if(reversible[pumpNum]){
    boolean reversed = pumpSpeeds[pumpNum] < 0;
    boolean enabled = !(abs(pumpSpeeds[pumpNum]) == 0);

    if(twoPinReverse[pumpNum]){
      digitalWrite(dirPins[pumpNum],reversed);
      digitalWrite(onOffPins[pumpNum],!reversed);
    }else{
      digitalWrite(dirPins[pumpNum],reversed);
      digitalWrite(onOffPins[pumpNum],enabled);
    }
  } 
}

void PumpController2::setPumpSpeed(int pumpNum, int pumpSpeed, boolean overide){
  if(pumpNum < 0 || pumpNum > totalPumps || pumpSpeed > 255 || pumpSpeed < -255) {
    return;
  }

  if((overide && pumpSpeeds[pumpNum] != pumpSpeed) || (!pumpOverides[pumpNum] && (pumpSpeeds[pumpNum] != pumpSpeed))){
    speedsChanged = true;
    pumpUpdateTime = millis();    
  }  
  
  if(pumpOverides[pumpNum] && !overide){  // if the pump is currently overidden
    nonOverideSpeeds[pumpNum] = pumpSpeed;
  }else if(!pumpOverides[pumpNum] && overide){
    nonOverideSpeeds[pumpNum] = pumpSpeeds[pumpNum];
    pumpSpeeds[pumpNum] = pumpSpeed;
  }else{
    pumpSpeeds[pumpNum] = pumpSpeed;
  }

  if(overide){
    pumpOverides[pumpNum] = overide;
  }else{
    nonOverideSpeeds[pumpNum] = pumpSpeed;
  }

  if(speedsChanged){
    applySpeedToPump(pumpNum);
  }

  
}



void PumpController2::releasePumpOverides(int pumpNum, boolean overide){
  if(pumpNum < 0 || pumpNum > totalPumps) {
      return;
  }
  if(!overide){
    pumpOverides[pumpNum] = false;
    pumpSpeeds[pumpNum] = nonOverideSpeeds[pumpNum];
    speedsChanged = true;
  }
  applySpeedToPump(pumpNum);
}

void PumpController2::dilute(int power){
  float workingValue = float(power) * float(maxDilutionPower)/255.0;
  dilutionPower = (byte) round(workingValue);
  dilutionFlag = true;
  dilutionStage = 0;  
}

void PumpController2::cycleSensors(){
  setPumpSpeed(0, -255, false);
  setPumpSpeed(3, -255, false);
  delay(5000);
  setPumpSpeed(0, 255, false);
  setPumpSpeed(3, 255, false);
  delay(5000);
}

void PumpController2::updatePumps(){
  
  latest_time = millis();  
  if (dilutionFlag) {
    if (dilutionStage == 0){
      dilutionStartTime = latest_time;
      setPumpSpeed(4, dilutionPower, false);
      speedsChanged = true;
      if (accrewedDilutionVolume[0] - accrewedDilutionVolume[2] > volumeOffsetThreshold || accrewedDilutionVolume[1] - accrewedDilutionVolume[2] > volumeOffsetThreshold){
        dilutionStage = 5;
        excessTimeNeeded = 60000*(max(accrewedDilutionVolume[0] - accrewedDilutionVolume[2], accrewedDilutionVolume[1] - accrewedDilutionVolume[2]))/pumpFullFlowRate[2];
      }else{
        dilutionStage = 1;
      }      
    }
    else if (dilutionStage == 1 && latest_time - dilutionStartTime > dilutionTime){
      accrewedDilutionVolume[2] += pump2sFlowRate[2]*2.0/60.0 + (latest_time - dilutionStartTime - 2000) * pumpFullFlowRate[2] /60000.0;
      setPumpSpeed(4, 0, false);
      dilutionStage = 2;
      dilutionStartTime = latest_time;
      setPumpSpeed(2, dilutionPower, false);
      if(mediaPrepSetup == 2){
        setPumpSpeed(1, dilutionPower, false);
      }
      speedsChanged = true;
    }else if (dilutionStage == 5 && latest_time - dilutionStartTime > dilutionTime + excessTimeNeeded){
      accrewedDilutionVolume[2] += pump2sFlowRate[2]*2.0/60.0 + (latest_time - dilutionStartTime - 2000) * pumpFullFlowRate[2] /60000.0;
      setPumpSpeed(4, 0, false);
      dilutionStage = 2;
      dilutionStartTime = latest_time;
      setPumpSpeed(2, dilutionPower, false);
      if(mediaPrepSetup == 2){
        setPumpSpeed(1, dilutionPower, false);
      }
      speedsChanged = true;
    }
    else if (dilutionStage == 2 && (latest_time - dilutionStartTime) > (dilutionTime)){    
      accrewedDilutionVolume[0] += pump2sFlowRate[0]*2.0/60.0 + (latest_time - dilutionStartTime - 2000) * pumpFullFlowRate[0] /60000.0;
      accrewedDilutionVolume[1] += pump2sFlowRate[1]*2.0/60.0 + (latest_time - dilutionStartTime - 2000) * pumpFullFlowRate[1] /60000.0;
      dilutionEndTime = latest_time;
      if((accrewedDilutionVolume[2] - accrewedDilutionVolume[0]) > volumeOffsetThreshold){
        setPumpSpeed(2, 0, false);
        speedsChanged = true;
        dilutionStage = 3;
        excessTimeNeeded = 60000*(accrewedDilutionVolume[2] - accrewedDilutionVolume[0])/pumpFullFlowRate[0];        
      }else if(accrewedDilutionVolume[2] - accrewedDilutionVolume[1] > volumeOffsetThreshold){
        setPumpSpeed(1, 0, false);
        speedsChanged = true;
        dilutionStage = 4;
        excessTimeNeeded = 60000*(accrewedDilutionVolume[2] - accrewedDilutionVolume[1])/pumpFullFlowRate[1];   
      }else{
        dilutionFlag = false;
        dilutionStage = 0;
        setPumpSpeed(2, 0, false);
        setPumpSpeed(1, 0, false);   
        speedsChanged = true;
      }      
    }else if (dilutionStage == 3 && (latest_time - dilutionEndTime) > excessTimeNeeded){
      accrewedDilutionVolume[0] += (latest_time - dilutionEndTime) * pumpFullFlowRate[0] /60000.0;
      setPumpSpeed(1, 0, false);
      speedsChanged = true;
      dilutionFlag = false;
      dilutionStage = 0;
    }else if (dilutionStage == 4 && (latest_time - dilutionEndTime) > excessTimeNeeded){
      setPumpSpeed(2, 0, false);
      speedsChanged = true;
      accrewedDilutionVolume[1] += (latest_time - dilutionEndTime) * pumpFullFlowRate[1] /60000.0;
      dilutionFlag = false;
      dilutionStage = 0;
    }
    
  }else if (fixedDilutionRateEnabled){
    if ((latest_time - dilutionStartTime + dilutionTime) > fixedDilutionRate){
      dilute(255);
    }
  }
  for(int i = 0; i < totalPumps; i++){
    if(latest_time > pumpOffTime[i]){
      speedsChanged = true;
      setPumpSpeed(i, 0, false);
      pumpOffTime[i] = 0;
    }
  }
}
