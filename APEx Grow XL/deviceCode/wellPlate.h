#include "config.h"

class WellPlate{
  public:
    WellPlate(int sWells_, int lWells_, float rowSpacing_, float columnSpacing_,float xFirstWellPos_, float yFirstWellPos_, float xLastWellPos_, float yLastWellPos_);
    WellPlate();
    boolean incrementWell();
    int getWell();
    boolean setWell(int wellID);

    float xCurWellPosition;
    float yCurWellPosition;

    int getRows();
    int getColumns();

    void setDimensions(int sWells_, int lWells_, float rowSpacing_, float columnSpacing_);
    void setFirstLastWell(float xFirstWellPos_, float yFirstWellPos_, float xLastWellPos_, float yLastWellPos_);

    
    
  private:
    int rows;
    int columns;
    float xFirstWellPos;
    float yFirstWellPos;
    float xLastWellPos;
    float yLastWellPos;

    float rowSpacing;
    float columnSpacing;

    float rowChangeXIncrement;
    float rowChangeYIncrement;

    float columnChangeXIncrement;
    float columnChangeYIncrement;

    int curWellID = 0;

    void calculateSpacing();
    boolean calculatePosition();
}; 
