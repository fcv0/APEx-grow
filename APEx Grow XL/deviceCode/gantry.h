#include <Stepper.h>

#include "config.h"
#include "pinMap.h"
#include "wellPlate.h"


class GantryController{
  public:
    GantryController(float xAxisLength_, int xStepsPerRev_, int xMaxRPM_, float xDistPerRev_, int xStepperPin1, int xStepperPin2,int xStepperPin3,int xStepperPin4, int xLimitPin_,
                     float yAyisLength_, int yStepsPerRev_, int yMaxRPM_, float yDistPerRev_, int yStepperPin1, int yStepperPin2,int yStepperPin3,int yStepperPin4, int yLimitPin_);
    GantryController();                     
                     
    void setAxisLength(bool axis, float axisLength);
    float getAxisLength(bool axis);

    void setStepsPerRev(bool axis, int stepsPerRev);
    int getStepsPerRev(bool axis);

    void setRPM(bool axis, int RPM);
    int getRPM(bool axis);

    void setDistPerRev(bool axis, float distPerRev);
    float getDistPerRev(bool axis);

    float getCurrentAxisPosition(bool axis);
    signed long getCurrentAxisSteps(bool axis);

    void homeAllAxes();
    void homeAxis(bool axis);

    void moveToPostion(float xPos, float yPos);  // given in physical units, cm
    void moveByDistance(float xDist, float yDist);  // given in physical units, cm
    void moveBySteps(float xSteps, float ySteps);

    void moveToPostion(bool axis, float pos);  // given in physical units, cm
    void moveByDistance(bool axis, float dist);  // given in physical units, cm
    void moveBySteps(bool axis, float steps);
    
    void setWellPlate(WellPlate wellPlate_);
    WellPlate getWellPlate();

    void moveToNextWell();

    void moveToWell(int wellID);

    void dryRun();
    
  
  private:
    Stepper xAxisStepper = Stepper(100, 5, 6);
    Stepper yAxisStepper = Stepper(100, 5, 6);

    float xAxisLength;
    int xStepsPerRev;
    int xMaxRPM;
    float xDistPerRev;
    int xLimitPin;
    signed long  xCurStep;    

    float yAxisLength;
    int yStepsPerRev;
    int yMaxRPM;
    float yDistPerRev;
    int yLimitPin;
    signed long yCurStep;    

    WellPlate wellPlate;
};
