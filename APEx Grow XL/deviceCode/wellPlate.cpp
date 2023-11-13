#include "wellPlate.h"

WellPlate::WellPlate(int sWells_, int lWells_, float rowSpacing_, float columnSpacing_,float xFirstWellPos_, float yFirstWellPos_, float xLastWellPos_, float yLastWellPos_){
  rows = sWells_;
  columns = lWells_;
  xFirstWellPos = xFirstWellPos_;
  yFirstWellPos = yFirstWellPos_;
  xLastWellPos = xLastWellPos_;
  yLastWellPos = yLastWellPos_;

  rowSpacing = rowSpacing_;
  columnSpacing = columnSpacing_;

  calculateSpacing();
}

WellPlate::WellPlate(){
  rows = 0;
  columns = 0;
  xFirstWellPos = 0;
  yFirstWellPos = 0;
  xLastWellPos = 0;
  yLastWellPos = 0;
}

int WellPlate::getWell(){
  return curWellID;
}

int WellPlate::getRows(){
  return rows;
}

int WellPlate::getColumns(){
  return columns;
}

boolean WellPlate::calculatePosition(){ 
  
  int columnNum = round(curWellID/rows + 0.5)-1;
  int rowNum = curWellID%rows;
  if (columnNum % 2 == 1){
    rowNum = (rows-1) - rowNum;
  }
//
//  Serial.print(curWellID);
//  Serial.print("\t");
//  Serial.print(rowNum);
//  Serial.print("\t");
//  Serial.print(columnNum);
//  Serial.print("\n");

  xCurWellPosition = rowNum * rowChangeXIncrement + columnNum * columnChangeXIncrement + xFirstWellPos;
  yCurWellPosition = rowNum * rowChangeYIncrement + columnNum * columnChangeYIncrement + yFirstWellPos;
  return true;
}

boolean WellPlate::incrementWell(){
  curWellID ++;
  if (curWellID == rows * columns){
    curWellID --;
    return false;
  }
  return calculatePosition();
}

boolean WellPlate::setWell(int wellID){
  curWellID  = wellID;
  return calculatePosition();
}

void WellPlate::setDimensions(int sWells_, int lWells_, float rowSpacing_, float columnSpacing_){
  rows = sWells_;
  columns = lWells_;

  rowSpacing = rowSpacing_;
  columnSpacing = columnSpacing_;

  calculateSpacing();
}

void WellPlate::setFirstLastWell(float xFirstWellPos_, float yFirstWellPos_, float xLastWellPos_, float yLastWellPos_){
  xFirstWellPos = xFirstWellPos_;
  yFirstWellPos = yFirstWellPos_;
  xLastWellPos = xLastWellPos_;
  yLastWellPos = yLastWellPos_;
  
  calculateSpacing();
}


void WellPlate::calculateSpacing(){
  float firstLastXDelta = xLastWellPos - xFirstWellPos;
  float firstLastYDelta = yLastWellPos - yFirstWellPos;

//  Serial.print(xLastWellPos);
//  Serial.print("\t");
//  Serial.print(xFirstWellPos);
//  Serial.print("\t");
//  Serial.print(firstLastXDelta);
//  Serial.print("\t");
//  Serial.print(yLastWellPos);
//  Serial.print("\t");
//  Serial.print(yFirstWellPos);
//  Serial.print("\t");
//  Serial.print(firstLastYDelta);
//  Serial.print("\n");

  float axisDiagonalDistance = sqrt(pow(firstLastXDelta,2) + pow(firstLastYDelta,2));
  float plateDiagonalDistance = sqrt(pow((rows-1) * rowSpacing,2) + pow((columns-1) * columnSpacing,2));

  float axisCrossingPointX = (xFirstWellPos + xLastWellPos)/2;
  float axisCrossingPointY = (yFirstWellPos + yLastWellPos)/2;

  float alpha = atan(((rows-1) * rowSpacing)/(firstLastYDelta - (columns-1)*columnSpacing));


  // calculating vectors from well to well

  float a = columnSpacing;
  float b = rowSpacing;

  rowChangeXIncrement = b * firstLastXDelta/abs(firstLastXDelta);
  rowChangeYIncrement = 0;

  columnChangeXIncrement = a/tan(alpha);//
  columnChangeYIncrement = a * sin(alpha) + a*cos(alpha)/tan(alpha);

//  Serial.print(alpha);
//  Serial.print("\t");
//  Serial.print(a);
//  Serial.print("\t");
//  Serial.print(b);
//  Serial.print("\n");
}
