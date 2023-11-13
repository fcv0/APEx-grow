#include "gantry.h"

GantryController::GantryController(float xAxisLength_, int xStepsPerRev_, int xMaxRPM_, float xDistPerRev_, int xStepperPin1, int xStepperPin2,int xStepperPin3,int xStepperPin4, int xLimitPin_,
                                   float yAxisLength_, int yStepsPerRev_, int yMaxRPM_, float yDistPerRev_, int yStepperPin1, int yStepperPin2,int yStepperPin3,int yStepperPin4, int yLimitPin_){
                      
  xAxisStepper = Stepper(xStepsPerRev_, xStepperPin1, xStepperPin2, xStepperPin3, xStepperPin4);
  yAxisStepper = Stepper(yStepsPerRev_, yStepperPin1, yStepperPin2, yStepperPin3, yStepperPin4);
  
  xAxisLength = xAxisLength_;
  xStepsPerRev = xStepsPerRev_;
  xMaxRPM = xMaxRPM_;
  xDistPerRev = xDistPerRev_;
  xLimitPin = xLimitPin_;
  xCurStep = 0;  
  
  yAxisLength = yAxisLength_;
  yStepsPerRev = yStepsPerRev_;
  yMaxRPM = yMaxRPM_;
  yDistPerRev = yDistPerRev_;
  yLimitPin = yLimitPin_;
  yCurStep = 0;     

  pinMode(xLimitPin, INPUT);
  pinMode(yLimitPin, INPUT);

  xAxisStepper.setSpeed(xMaxRPM);
  yAxisStepper.setSpeed(yMaxRPM);
  
//  homeAllAxes();
}

GantryController::GantryController(){
  
}

void GantryController::homeAllAxes(){
  bool homedX = false;
  bool homedY = false; 

  float moveSize = 0.1; //cm

  while(!homedX || !homedY){
    if (!homedX && !homedY){
      moveByDistance((float)-moveSize, -moveSize);
      homedX = digitalRead(xLimitPin) == HIGH;
      homedY = digitalRead(yLimitPin) == HIGH;
    }
    else{
      if (!homedX){
        moveByDistance(X, -moveSize);
        homedX = digitalRead(xLimitPin) == HIGH; 
      }
      if (!homedY){
        moveByDistance(Y, -moveSize);
        homedY = digitalRead(yLimitPin) == HIGH; 
      }
    }
  }

  moveByDistance((float) 10 * moveSize, 10 * moveSize);
  
  homedX = false;
  homedY = false;
  while(!homedX || !homedY){
    if (!homedX && !homedY){
      moveByDistance((float)-moveSize/4, -moveSize/4);
      homedX = digitalRead(xLimitPin) == HIGH;
      homedY = digitalRead(yLimitPin) == HIGH;
    }
    else{
      if (!homedX){
        moveByDistance(X, -moveSize/4);
        homedX = digitalRead(xLimitPin) == HIGH; 
      }
      if (!homedY){
        moveByDistance(Y, -moveSize/4);
        homedY = digitalRead(yLimitPin) == HIGH; 
      }
    }
  }
  xCurStep = 0;  
  yCurStep = 0;

  moveByDistance((float) 10 * moveSize, 10 * moveSize);
  
}

void GantryController::homeAxis(bool axis){
  bool homed = false;

  float moveSize = 0.1; //cm

  while(!homed){
    moveByDistance(axis, -moveSize);
    if (axis == X){
      homed = digitalRead(xLimitPin) == HIGH;  
    }else{
      homed = digitalRead(yLimitPin) == HIGH;    
    }
  }

  moveByDistance(axis, 10 * moveSize);
  
  homed = false;
  while(!homed){
    moveByDistance(axis, -moveSize/4);
    if (axis == X){
      homed = digitalRead(xLimitPin) == HIGH;  
    }else{
      homed = digitalRead(yLimitPin) == HIGH;    
    }
  }

  if (axis == X){
    xCurStep = 0;  
  }else{
    yCurStep = 0;
  }

  moveByDistance(axis, 10 * moveSize);
  
}

//void GantryController::moveToPostion(float xPos, float yPos){
//  if(xPos < 0 || xPos > xAxisLength or yPos < 0 || yPos > yAxisLength){
//    return;
//  }
//  
//  float xDelta = getCurrentAxisPosition(X) - xPos;
//  float yDelta = getCurrentAxisPosition(Y) - yPos;
//
//  float largestMoveDist = max(abs(xDelta), abs(xDelta));
//
//  int xSteps = 0;
//  int ySteps = 0;
// 
//  if(largestMoveDist < axisMoveSize){
//    xSteps = round(xDelta/xDistPerRev * xStepsPerRev);
//    xAxisStepper.step(xSteps);
//    
//    ySteps = round(yDelta/yDistPerRev * yStepsPerRev);
//    xAxisStepper.step(ySteps);
//
//    xCurStep += xSteps;
//
//  }else{
//    float xDistToMove = axisMoveSize * abs(xDelta)/largestMoveDist;
//    xSteps = round(xDistToMov/xDistPerRev * xStepsPerRev);
//    xAxisStepper.step(xSteps);
//
//    float yDistToMove = axisMoveSize * abs(yDelta)/largestMoveDist;
//    ySteps = round(yDistToMove/yDistPerRev * yStepsPerRev);
//    yAxisStepper.step(ySteps);    
//  }   
//  xCurStep += xSteps;
//  yCurStep += ySteps;
//}

void GantryController::moveToPostion(float xPos, float yPos){
  if(xPos < 0 || xPos > xAxisLength or yPos < 0 || yPos > yAxisLength){
    return;
  }

//  Serial.print(getCurrentAxisPosition(X));
//  Serial.print("\t");
//  Serial.print(getCurrentAxisPosition(Y));
//  Serial.print("\t");
//  Serial.print(xPos);
//  Serial.print("\t");
//  Serial.print(yPos);
//  Serial.print("\t");

//  Serial.print(xPos);
//  Serial.print("\t");
//  Serial.print(yPos);
//  Serial.print("\n");
  
  float xDelta = xPos - getCurrentAxisPosition(X);
  float yDelta = yPos - getCurrentAxisPosition(Y);

  moveByDistance(xDelta,yDelta);
}

void GantryController::moveByDistance(float xDist, float yDist){
  float xSteps = xDist* xStepsPerRev;
  xSteps /= xDistPerRev;
  float ySteps = yDist * yStepsPerRev;
  ySteps /= yDistPerRev;

//  Serial.print(xDist);
//  Serial.print("\t");
//  Serial.print(yDist);
//  Serial.print("\t");
//  Serial.print(xSteps);
//  Serial.print("\t");
//  Serial.print(ySteps);
//  Serial.print("\n");

  moveBySteps(xSteps, ySteps);
}

void GantryController::moveBySteps(float xSteps, float ySteps){
  long xStepsInt = round(xSteps);
  long yStepsInt = round(ySteps); 
  
  if (yStepsInt == 0){
    xAxisStepper.step(-xStepsInt);
  }else if (xStepsInt == 0){
    yAxisStepper.step(-yStepsInt);
  }else{
//    Serial.print(xStepsInt);
//    Serial.print("\t");
//    Serial.print(yStepsInt);
//    Serial.print("\n");
    long xStepsDone = 0;
    long yStepsDone = 0;
    float fidelity = max(abs(xSteps),abs(ySteps));
    for(long i = 0; i < fidelity; i++){
//      Serial.print(i);
//      Serial.print("\t");
//      Serial.print(fidelity);
//      Serial.print("\t");
//      Serial.print(i/fidelity);
//      Serial.print("\t");
//      Serial.print((float)i/fidelity);
//      Serial.print("\t");

      float xStepsFraction = ((float) xStepsDone)/abs(xStepsInt);
      float yStepsFraction = ((float) yStepsDone)/abs(yStepsInt);
      
//      Serial.print(xStepsFraction);
//      Serial.print("\t");
//      Serial.print(yStepsFraction);
//      Serial.print("\t");
      
      if(xStepsFraction <= i/fidelity){
         float stepsToDo = round(((i/fidelity) - xStepsFraction) *abs(xStepsInt) * xStepsInt/abs(xStepsInt)) ;
         xAxisStepper.step(-round(stepsToDo));
         xStepsDone += abs(stepsToDo);
      }
      if(yStepsFraction <= i/fidelity){
         float stepsToDo = round(((i/fidelity) - yStepsFraction) *abs(yStepsInt) * yStepsInt/abs(yStepsInt));
         yAxisStepper.step(-stepsToDo);
         yStepsDone += abs(stepsToDo);
      }
//      Serial.print(xStepsDone);
//      Serial.print("\t");
//      Serial.print(yStepsDone);
//      Serial.print("\t");
//      Serial.print(xStepsInt);
//      Serial.print("\t");
//      Serial.print(yStepsInt);
//      Serial.print("\n");
    }
    if(xStepsDone < abs(xStepsInt)){
      xAxisStepper.step(-xStepsInt/abs(xStepsInt) * (abs(xStepsInt) - xStepsDone));
    }
  
    if(yStepsDone < abs(yStepsInt)){
      yAxisStepper.step(-yStepsInt/abs(yStepsInt) * (abs(yStepsInt) - yStepsDone));
    }
  }
  
  
  xCurStep += xStepsInt;
  yCurStep += yStepsInt;
}

void GantryController::moveToPostion(bool axis, float pos){
  if(axis == X){
    moveToPostion(pos, getCurrentAxisPosition(Y));
  }else{
    moveToPostion(getCurrentAxisPosition(Y), pos);
  }
}

void GantryController::moveByDistance(bool axis, float dist){
  if(axis == X){
    moveByDistance(dist, 0);
  }else{
    moveByDistance((float) 0, dist);
  }
}

void GantryController::moveBySteps(bool axis, float steps){
  if(axis == X){
    moveBySteps(steps, 0);
  }else{
    moveBySteps((float)0, steps);
  }
}

void GantryController::setAxisLength(bool axis, float axisLength){
  if(axis == X){
    xAxisLength = axisLength;
  }else{
    yAxisLength = axisLength;
  }
}
float GantryController::getAxisLength(bool axis){
  if(axis == X){
    return xAxisLength;
  }else{
    return yAxisLength;
  }
}

void GantryController::setStepsPerRev(bool axis, int stepsPerRev){
  if(axis == X){
    xStepsPerRev = stepsPerRev;
  }else{
    yStepsPerRev = stepsPerRev;
  }
}

int GantryController::getStepsPerRev(bool axis){
  if(axis == X){
    return xStepsPerRev;
  }else{
    return yStepsPerRev;
  }
}

void GantryController::setRPM(bool axis, int RPM){
  if(axis == X){
    xMaxRPM = RPM;
  }else{
    yMaxRPM = RPM;
  }
}
int GantryController::getRPM(bool axis){
  if(axis == X){
    return xMaxRPM;
  }else{
    return yMaxRPM;
  }
}

void GantryController::setDistPerRev(bool axis, float distPerRev){
  if(axis == X){
    xDistPerRev = distPerRev;
  }else{
    yDistPerRev = distPerRev;
  }
}
float GantryController::getDistPerRev(bool axis){
  if(axis == X){
    return xDistPerRev;
  }else{
    return yDistPerRev;
  }
}

float GantryController::getCurrentAxisPosition(bool axis){
  if(axis == X){
    return (xCurStep * xDistPerRev) / xStepsPerRev;
  }else{
    return (yCurStep * yDistPerRev) / yStepsPerRev ;
  }
}

signed long GantryController::getCurrentAxisSteps(bool axis){
  if(axis == X){
    return xCurStep;
  }else{
    return yCurStep;
  }
}


void GantryController::setWellPlate(WellPlate wellPlate_){
  wellPlate = wellPlate_;
}


WellPlate GantryController::getWellPlate(){
  return wellPlate;
}


void GantryController::moveToNextWell(){
  wellPlate.incrementWell();
//  Serial.print(wellPlate.xCurWellPosition);
//  Serial.print("\t");
//  Serial.print(wellPlate.yCurWellPosition);
//  Serial.print("\n");
  moveToPostion(wellPlate.xCurWellPosition, wellPlate.yCurWellPosition);
}

void GantryController::moveToWell(int wellID){
  wellPlate.setWell(wellID);
//  Serial.print(wellPlate.xCurWellPosition);
//  Serial.print("\t");
//  Serial.print(wellPlate.yCurWellPosition);
//  Serial.print("\n");
  moveToPostion(wellPlate.xCurWellPosition, wellPlate.yCurWellPosition);
}


void GantryController::dryRun(){
  moveToWell(0);
  delay(500);

  for(int i = 0; i < (wellPlate.getRows() * wellPlate.getRows() - 1); i ++){
    moveToNextWell();
    delay(500);
  }
}
