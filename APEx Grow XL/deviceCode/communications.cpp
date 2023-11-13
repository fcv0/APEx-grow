#include "config.h"
#include "communications.h"


CommunicationHandler::CommunicationHandler(){
  
}

void CommunicationHandler::cycle(){  

  if (commsTurn){
    encodeOutbound();
    Serial.write(outbound,60);
    flushInputBuffer();
    commsTurn = false;
  }    
  if (!commsTurn && Serial.available() >= 60){
    Serial.readBytes(inbound, 60);
    if (validateInbound()){
       extractInbound();
    }
    else{
      extractInbound();
//       pass // add proper error flags here
    }
    commsTurn = true;
  }
}

void CommunicationHandler::addToStdBuffer(byte code){
  if(standardOutBuffer_i == 39){
    return;
  }
  if(standardOutBuffer[standardOutBuffer_i] == code){
    return;
  }
  standardOutBuffer_i = standardOutBuffer_i + 1;
  standardOutBuffer[standardOutBuffer_i] = code;
//  for(int i = standardOutBuffer_i - 1; i > 0;  i --){
//    if(standardOutBuffer[i] == code){
//      standardOutBuffer[i] = 223;  // skip code
//    }
//  }
}

void CommunicationHandler::addToPriorityBuffer(byte code){
  if(priorityOutBuffer_i == 39){
    return;
  }
  priorityOutBuffer_i++;
  priorityOutBuffer[priorityOutBuffer_i] = code;
}

int CommunicationHandler::combineBytesToInt(byte byte1, byte byte2){
  int a = 0;
  a = a | byte1;
  a = a << 8;
  a = a | byte2;
  return a;  
}

unsigned long CommunicationHandler::combineBytesToLong(byte byte1, byte byte2, byte byte3, byte byte4){
  unsigned long a = 0;
  a = a | byte1;
  a = a << 8;
  a = a | byte2;
  a = a << 8;
  a = a | byte3;
  a = a << 8;
  a = a | byte4;
  return a;  
}

float CommunicationHandler::combineBytesToFloat(byte byte1, byte byte2, byte byte3, byte byte4){
  unsigned long val = combineBytesToLong(byte1, byte2, byte3, byte4);
  float * floatPtr;
  floatPtr = (float*) &val;
  float val2 = *floatPtr;
  return val2;
}

void CommunicationHandler::placeLongInOutbound(unsigned long val, int index1, int index2, int index3, int index4){
  byte byte4 = 0;
  byte4 = (val & 0b11111111);
  byte byte3 = 0;
  byte3 = (val & 0b1111111100000000)>>8;
  byte byte2 = 0;
  byte2 = (val & 0b111111110000000000000000)>>16;
  byte byte1 = 0;
  byte1 = (val & 0b11111111000000000000000000000000)>>24;

  outbound[index1] = byte1;
  outbound[index2] = byte2;
  outbound[index3] = byte3;
  outbound[index4] = byte4;
}

void CommunicationHandler::placeFloatInOutbound(float val, int index1, int index2, int index3, int index4){
  unsigned long val2;
  unsigned long * longPtr;
  longPtr = (unsigned long*) &val;
  val2 = *longPtr;
  
  placeLongInOutbound(val2, index1, index2, index3, index4);
}

void CommunicationHandler::placeIntInOutbound(int val, int index1, int index2){
  byte byte2 = 0;
  byte2 = (val & 0b11111111);
  byte byte1 = 0;
  byte1 = (val & 0b1111111100000000)>>8;

  outbound[index1] = byte1;
  outbound[index2] = byte2;
}

void CommunicationHandler::encodeOutbound(){
  if (standardOutBuffer_i == 39){
    for(int i = 0; i < 40; i++){
      standardOutBuffer[i] = 0;
    }
    standardOutBuffer_i = 1;
  }
  for(int i = 0; i < 60; i++){
    outbound[i] = 0;
  }
  byte outboundStatus = 0;

  if (runInProgress){
    outboundStatus = 1;
  }

  if (priorityOutBuffer_i > 0) {
    outboundStatus = priorityOutBuffer[priorityOutBuffer_i];
    priorityOutBuffer_i--;
  }else if(standardOutBuffer_i > 0) {
    outboundStatus = standardOutBuffer[standardOutBuffer_i];
    standardOutBuffer_i--;
//    while(outboundStatus == 223){
//      outboundStatus = standardOutBuffer[standardOutBuffer_i];
//      standardOutBuffer_i--;
//    }
  }

  outbound[0] = outboundStatus;
  placeLongInOutbound(millis(),1,2,3,4);

  

  switch(outboundStatus){
    case 0: // standard
    case 1:       // run in progress       
    case 10:    // pumps updated 
      placeFloatInOutbound(tempControl.target,5,6,7,8);   
      placeIntInOutbound(tempControl.heaterPower,9,10);
      placeIntInOutbound(tempControl.heaterPowerSet,11,12);

      for(int i = 0; i < totalPumps; i ++){
        outbound[13 + i] = abs(pumpController.pumpSpeeds[i]);
        outbound[13 + i + totalPumps] = (pumpController.pumpSpeeds[i] < 0) ? 1 : 0;
      }
      placeFloatInOutbound(tempControlMedia.target,31,32,33,34);
      placeIntInOutbound(tempControlMedia.heaterPower,35,36);
      placeIntInOutbound(tempControlMedia.heaterPowerSet,37,38);
      placeFloatInOutbound(ODControl.target,39,40,41,42);
      if(outboundStatus == 10){
        pumpController.speedsChanged = false;
        placeLongInOutbound(pumpController.pumpUpdateTime,43,44,45,46);
      }else{
        placeLongInOutbound(millis(),43,44,45,46);      
      }
      break;
    case 4:       //OD transmit
      placeLongInOutbound(lastODSample, 5,6,7,8);
      placeFloatInOutbound(ODs[0], 9,10,11,12);
      placeFloatInOutbound(ODs[1], 13,14,15,16);
      placeFloatInOutbound(ODs[2], 17,18,19,20);
      placeFloatInOutbound(ODs[3], 21,22,23,24);
      placeFloatInOutbound(ODs[4], 25,26,27,28);
      placeFloatInOutbound(ODs[5], 29,30,31,32);
      placeFloatInOutbound(rawODs[0], 33,34,35,36);
      placeFloatInOutbound(rawODs[1], 37,38,39,40);
      placeFloatInOutbound(rawODs[2], 41,42,43,44);
      placeFloatInOutbound(rawODs[3], 45,46,47,48);
      placeFloatInOutbound(rawODs[4], 49,50,51,52);
      placeFloatInOutbound(rawODs[5], 53,54,55,56);
      newODToSend = false;
      break;
    case 5:       //raw photodiode values transmit
      placeLongInOutbound(lastODSample, 5,6,7,8);
      placeFloatInOutbound(absorb[0], 9,10,11,12);
      placeFloatInOutbound(absorb[1], 13,14,15,16);
      placeFloatInOutbound(absorb[2], 17,18,19,20);
      placeFloatInOutbound(absorb[3], 21,22,23,24);
      placeFloatInOutbound(absorb[4], 25,26,27,28);
      placeFloatInOutbound(absorb[5], 29,30,31,32);
      placeFloatInOutbound(scatter[0], 33,34,35,36);
      placeFloatInOutbound(scatter[1], 37,38,39,40);
      placeFloatInOutbound(scatter[2], 41,42,43,44);
      placeFloatInOutbound(scatter[3], 45,46,47,48);
      placeFloatInOutbound(scatter[4], 49,50,51,52);
      placeFloatInOutbound(scatter[5], 53,54,55,56);
      break;
    
    case 6:   // temperature data transmit
      placeLongInOutbound(lastTempSample, 5,6,7,8);
      placeFloatInOutbound(curTemp, 9,10,11,12);
      placeIntInOutbound(curTempRaw,13,14);
      placeIntInOutbound(curTempRawHeaterPower,15,16);
      placeIntInOutbound(curTempRawHeaterPowerSet,17,18);
      placeFloatInOutbound(curTempIR, 19,20,21,22);
      placeFloatInOutbound(curAmbientTempIR, 23,24,25,26);
      newTempToSend = false;
      break;

     case 7:       //OD transmit media
      placeLongInOutbound(lastODSampleMedia, 5,6,7,8);
      placeFloatInOutbound(ODsMedia[0], 9,10,11,12);
      placeFloatInOutbound(ODsMedia[1], 13,14,15,16);
      placeFloatInOutbound(ODsMedia[2], 17,18,19,20);
      placeFloatInOutbound(ODsMedia[3], 21,22,23,24);
      placeFloatInOutbound(ODsMedia[4], 25,26,27,28);
      placeFloatInOutbound(ODsMedia[5], 29,30,31,32);
      placeFloatInOutbound(rawODsMedia[0], 33,34,35,36);
      placeFloatInOutbound(rawODsMedia[1], 37,38,39,40);
      placeFloatInOutbound(rawODsMedia[2], 41,42,43,44);
      placeFloatInOutbound(rawODsMedia[3], 45,46,47,48);
      placeFloatInOutbound(rawODsMedia[4], 49,50,51,52);
      placeFloatInOutbound(rawODsMedia[5], 53,54,55,56);
      newODToSend = false;
      break;

     case 8:       //raw photodiode values transmit media
      placeLongInOutbound(lastODSampleMedia, 5,6,7,8);
      placeFloatInOutbound(absorbMedia[0], 9,10,11,12);
      placeFloatInOutbound(absorbMedia[1], 13,14,15,16);
      placeFloatInOutbound(absorbMedia[2], 17,18,19,20);
      placeFloatInOutbound(absorbMedia[3], 21,22,23,24);
      placeFloatInOutbound(absorbMedia[4], 25,26,27,28);
      placeFloatInOutbound(absorbMedia[5], 29,30,31,32);
      placeFloatInOutbound(scatterMedia[0], 33,34,35,36);
      placeFloatInOutbound(scatterMedia[1], 37,38,39,40);
      placeFloatInOutbound(scatterMedia[2], 41,42,43,44);
      placeFloatInOutbound(scatterMedia[3], 45,46,47,48);
      placeFloatInOutbound(scatterMedia[4], 49,50,51,52);
      placeFloatInOutbound(scatterMedia[5], 53,54,55,56);
      break;
    
    

     case 9:   // temperature data transmit
      placeLongInOutbound(lastTempSampleMedia, 5,6,7,8);
      placeFloatInOutbound(curTempMedia, 9,10,11,12);
      placeIntInOutbound(curTempRawMedia,13,14);
      placeIntInOutbound(curTempRawHeaterPowerMedia,15,16);
      placeIntInOutbound(curTempRawHeaterPowerSetMedia,17,18);
      placeFloatInOutbound(curTempIRMedia, 19,20,21,22);
      placeFloatInOutbound(curAmbientTempIRMedia, 23,24,25,26);
      newTempToSendMedia = false;
      break;
  }

  unsigned int checksum = fletcherChecksum(outbound,58);
  placeIntInOutbound(checksum,58,59);
  
}

boolean CommunicationHandler::validateInbound(){
  unsigned int checksum = fletcherChecksum(inbound,58);
  unsigned int promisedChecksum = combineBytesToInt(inbound[58],inbound[59]);

  boolean valid = !(checksum ^ promisedChecksum);

  return valid;  
}

void CommunicationHandler::extractInbound(){
  PCStatus = inbound[0];
  PCTime = combineBytesToLong(inbound[1],inbound[2],inbound[3],inbound[4]);  
  switch(PCStatus){
    case 2:
      runStartFlag = true;
      addToPriorityBuffer(2);
      break;
    case 3:
      runStopFlag = true;
      addToPriorityBuffer(3);
      break;
    case 4:  // pump overide
    {
      boolean overide = false;
      int pumpSpeed = 0;
      for(int i = 0; i < totalPumps; i++){
        overide = (inbound[5 + i] == 1);
        pumpSpeed = inbound[5 + totalPumps + i];
        if (inbound[5 + 2 * totalPumps + i] == 1){
          pumpSpeed *= -1;
        }
        if (overide){
          pumpController.setPumpSpeed(i, pumpSpeed, overide);
        }else{
          pumpController.releasePumpOverides(i, overide);  
        }
      }     
      break;
    }  
    case 5: //Motor Run For Duration
    {
      int pumpNum = inbound[5];
      int pumpSpeed = inbound[6];
      unsigned long pumpRunTime = combineBytesToLong(inbound[7],inbound[8],inbound[9], inbound[10]);
      pumpController.setPumpSpeed(pumpNum, pumpSpeed, false);
      pumpController.pumpOffTime[pumpNum] = millis() + pumpRunTime;
      break;
    }
    case 32:    // run transmit incomming start
      sequenceLength = combineBytesToInt(inbound[32],inbound[33]);
      sequenceHandler = SequenceHandler(inbound, 60, sequenceLength);
      addToPriorityBuffer(32);
      break;
    case 33:    // run transmit incomming end
      sequenceHandler.addSequence(inbound, 60);
      addToPriorityBuffer(33);
      break;
    case 34:    // run transmit incomming mid sequence
      sequenceHandler.addSequence(inbound, 60);
      addToPriorityBuffer(34);
      break;
    case 48:   //tempCalibration
      tempCalibrationGradient = combineBytesToFloat(inbound[5],inbound[6],inbound[7],inbound[8]);
      tempCalibraitonOffset = combineBytesToFloat(inbound[9],inbound[10],inbound[11],inbound[12]);   
      break;
    case 49:   // temp target
      tempControl.setTarget(((float)((inbound[5] << 8) | inbound[6])) / 10);
      tempControlMedia.setTarget(((float)((inbound[5] << 8) | inbound[6])) / 10);
      break;
    case 50:    //temp PID
      p = combineBytesToFloat(inbound[5],inbound[6],inbound[7],inbound[8]);
      i = combineBytesToFloat(inbound[9],inbound[10],inbound[11],inbound[12]);   
      d = combineBytesToFloat(inbound[13],inbound[14],inbound[15],inbound[16]);  
      if(inbound[17] == 255){        
        tempControl.setModePID(p,i,d);
        tempControl.pid.resetIntegral();
      }else{
        tempControl.setModeOnOff();
      }
      break;
    case 64:   //OD Calibration
      ODCalibrationGradient = combineBytesToFloat(inbound[5],inbound[6],inbound[7],inbound[8]);
      ODCalibraitonOffset = combineBytesToFloat(inbound[9],inbound[10],inbound[11],inbound[12]);   
      ODReferenceAbsorbance[0] = combineBytesToFloat(inbound[13],inbound[14],inbound[15],inbound[16]); 
      for(int i = 0; i < 6; i ++){
          ODReferenceAbsorbance[i] = ODReferenceAbsorbance[0];
          ODReferenceAbsorbanceMedia[i] = ODReferenceAbsorbance[0];
      }
      break;
    case 65:   //target OD
      ODControl.setTarget(((float)((inbound[5] << 8) | inbound[6])) / 100);
      break;
    case 66:    //OD PID
      p = combineBytesToFloat(inbound[5],inbound[6],inbound[7],inbound[8]);
      i = combineBytesToFloat(inbound[9],inbound[10],inbound[11],inbound[12]);   
      d = combineBytesToFloat(inbound[13],inbound[14],inbound[15],inbound[16]);
      if(inbound[17] == 255){
        ODControl.setModePID(p,i,d);
      }else{
        ODControl.setModeOnOff();
      }      
      break;

    case 68:
      reReferanceOD = true;
      break;
    case 69:
      reReferanceODMedia = true;
      break;
    case 80:
    //connect dissconect fossil record
      if(inbound[5] == 0){
        fossilRecordConnected = false;   
        firstWellProvided = false;
        lastWellProvided = false;     
      }else if(inbound[5] == 1){
        wellPlateRows = inbound[6];
        wellPlateColumns = inbound[7];
        wellPlateRowSpacing = combineBytesToFloat(inbound[8],inbound[8],inbound[10],inbound[11]);
        wellPlateColumnSpacing = combineBytesToFloat(inbound[12],inbound[13],inbound[14], inbound[15]);
        float gantrySizeX = combineBytesToFloat(inbound[16],inbound[17],inbound[18],inbound[19]);
        float gantrySizeY = combineBytesToFloat(inbound[20],inbound[21],inbound[22],inbound[23]);
        int stepsX = combineBytesToInt(inbound[24], inbound[25]);
        int stepsY = combineBytesToInt(inbound[26], inbound[27]);
        float motorRPMX = combineBytesToFloat(inbound[28],inbound[29],inbound[30],inbound[31]);
        float motorRPMY  = combineBytesToFloat(inbound[32],inbound[33],inbound[34],inbound[35]);
        float distPerRevX = combineBytesToFloat(inbound[36],inbound[37],inbound[38],inbound[39]);
        float distPerRevY = combineBytesToFloat(inbound[40],inbound[41],inbound[42],inbound[43]);

//        fossilRecord = GantryController(gantrySizeX,stepsX,motorRPMX,distPerRevX, stepperXPin1,stepperXPin2,stepperXPin3,stepperXPin4,limitPinX,
//                                        gantrySizeY,stepsY,motorRPMY,distPerRevY, stepperYPin1,stepperYPin2,stepperYPin3,stepperYPin4,limitPinY);
//        
      }
      break;
    case 81:
    // move fossil record by distance
  
      moveX = combineBytesToFloat(inbound[5],inbound[6],inbound[7],inbound[8]);
      moveY = combineBytesToFloat(inbound[9],inbound[10],inbound[11],inbound[12]);
  
      fossilRecord.moveByDistance(moveX,moveY);
      break;

    case 82:
    // move fossil record by steps
  
      moveX = combineBytesToLong(inbound[5],inbound[6],inbound[7],inbound[8]);
      moveY = combineBytesToLong(inbound[9],inbound[10],inbound[11],inbound[12]);
  
      fossilRecord.moveBySteps(moveX,moveY);
      break;

    case 83:
    // move fossil record to position
  
      moveX = combineBytesToFloat(inbound[5],inbound[6],inbound[7],inbound[8]);
      moveY = combineBytesToFloat(inbound[9],inbound[10],inbound[11],inbound[12]);
  
      fossilRecord.moveToPostion(moveX,moveY);
      break;

    case 85:
    //Set current position as first/ last well
      if(inbound[5] == 1){
        firstWellX = fossilRecord.getCurrentAxisPosition(X);
        firstWellY = fossilRecord.getCurrentAxisPosition(Y);
        firstWellProvided = true;
      }else if (inbound[5] == 0){
        lastWellX = fossilRecord.getCurrentAxisPosition(X);
        lastWellY = fossilRecord.getCurrentAxisPosition(Y);
        lastWellProvided = true;
      }

      if(firstWellProvided && lastWellProvided){
        wellPlate = WellPlate(wellPlateRows,wellPlateColumns, wellPlateRowSpacing,wellPlateColumnSpacing,
                              firstWellX,firstWellY,lastWellX,lastWellY);
        fossilRecord.setWellPlate(wellPlate);
      }
      break;
     
    case 89:
     //Perform a  dry run
        fossilRecord.dryRun();
        break;

    case 94:
     //set well plate dimensions
        wellPlateRows = inbound[5];
        wellPlateColumns = inbound[6];
        wellPlateRowSpacing = combineBytesToFloat(inbound[7],inbound[8],inbound[9],inbound[10]);
        wellPlateColumnSpacing = combineBytesToFloat(inbound[11],inbound[12],inbound[13],inbound[14]);
        fossilRecord.getWellPlate().setDimensions(wellPlateRows,wellPlateColumns,wellPlateRowSpacing,wellPlateColumnSpacing);
        break;

//    case 67: //Dilution Parameters
//    
//      if (inbound[5] == 1){
//        //constant dilution mode
//        ODControl.pumpController.fixedDilutionRateEnabled = true;
//        ODControl.pumpController.fixedDilutionRate = combineBytesToLong(inbound[6], inbound[7], inbound[8], inbound[9]);
//      }else{
//        ODControl.pumpController.fixedDilutionRateEnabled = false;
//      }
//      ODControl.pumpController.fixedDilutionRateEnabled = false;
//      ODControl.pumpController.dilutionTime = combineBytesToLong(inbound[10], inbound[11], inbound[12], inbound[13]);
//      ODControl.pumpController.maxDilutionPower = inbound[14];
//      break;

    //default: add status unknown return code 
    
  }  
}


void CommunicationHandler::flushInputBuffer(){
  while(Serial.available() > 0){
    Serial.read();
  }
}

unsigned int CommunicationHandler::fletcherChecksum(byte data[60], int count){
  
   unsigned int sum1 = 0;
   unsigned int sum2 = 0;
   int index;

   for ( index = 0; index < count; ++index )
   {
      sum1 = (sum1 + data[index]) % 255;
      sum2 = (sum2 + sum1) % 255;
   }

   return (sum2 << 8) | sum1;
}
