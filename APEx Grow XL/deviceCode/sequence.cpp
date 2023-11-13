#include "sequence.h"


Sequence::Sequence(byte data[], int arraySize) {
  num = data[5];
  timeTrigger = combineBytesToLong(data[6], data[7], data[8], data[9]);
  tempTrigger = ((float)((data[10] << 8) | data[11])) / 10;
  OD1Trigger = ((float)((data[12] << 8) | data[13])) / 100;
  OD2Trigger = ((float)((data[14] << 8) | data[15])) / 100;
  OD3Trigger = ((float)((data[16] << 8) | data[17])) / 100;
  OD4Trigger = ((float)((data[18] << 8) | data[19])) / 100;
  OD5Trigger = ((float)((data[20] << 8) | data[21])) / 100;
  OD6Trigger = ((float)((data[22] << 8) | data[23])) / 100;
  tempTarget = ((float)((data[24] << 8) | data[25])) / 10;
  ODSensor = data[26];
  ODTarget = ((float)((data[27] << 8) | data[28])) / 100;
  ODDrift = ((float)((data[29] << 8) | data[30])) / 100;
  next = data[31];
}

Sequence::Sequence() {
}

unsigned long Sequence::combineBytesToLong(byte byte1, byte byte2, byte byte3, byte byte4) {
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

SequenceHandler::SequenceHandler(byte data[], int arraySize, int seqLen) {
  totalSequenceNumber = seqLen;
  addSequence(data, arraySize);
}

SequenceHandler::SequenceHandler() {
}

void SequenceHandler::addSequence(byte data[], int arraySize) {
  sequenceArray[sequenceEnd_i] = Sequence(data, arraySize);
  sequenceEnd_i++;
}

void SequenceHandler::updateCurrentSequence(float temp, float OD1, float OD2, float OD3, float OD4, float OD5, float OD6) {
  newSequence = false;

  for (int i = 0; i < sequenceEnd_i; i++) {
    seqTimeLeft = sequenceArray[i].timeTrigger * 1000 - (millis() - seqStartTime);
    if (sequenceArray[i].num == sequenceArray[currentSeq_i].next) {   
//      digitalWrite(13, HIGH);
//      delay(200);
//      digitalWrite(13, LOW);   
      if (sequenceArray[i].timeTrigger * 1000 < millis() - seqStartTime) {
        currentSeq_i = i;
        newSequence = true;
        break;
      }
      else if ((sequenceArray[i].tempTrigger - temp) * (sequenceArray[i].tempTrigger - initialTemp) < 0) {
        currentSeq_i = i;
        newSequence = true;
        break;
      }
      else if ((sequenceArray[i].OD1Trigger - OD1) * (sequenceArray[i].OD1Trigger - initialOD1) < 0) {
        currentSeq_i = i;
        newSequence = true;
        break;
      }
      else if ((sequenceArray[i].OD2Trigger - OD2) * (sequenceArray[i].OD2Trigger - initialOD2) < 0) {
        currentSeq_i = i;
        newSequence = true;
        break;
      }
      else if ((sequenceArray[i].OD3Trigger - OD3) * (sequenceArray[i].OD3Trigger - initialOD3) < 0) {
        currentSeq_i = i;
        newSequence = true;
        break;
      }
      else if ((sequenceArray[i].OD4Trigger - OD4) * (sequenceArray[i].OD4Trigger - initialOD4) < 0) {
        currentSeq_i = i;
        newSequence = true;
        break;
      }
      else if ((sequenceArray[i].OD5Trigger - OD5) * (sequenceArray[i].OD5Trigger - initialOD5) < 0) {
        currentSeq_i = i;
        newSequence = true;
        break;
      }
      else if ((sequenceArray[i].OD6Trigger - OD6) * (sequenceArray[i].OD6Trigger - initialOD6) < 0) {
        currentSeq_i = i;
        newSequence = true;
        break;
      }
    }
  }

  if (newSequence) {
    tempTarget =  sequenceArray[currentSeq_i].tempTarget;
    ODSensor =  sequenceArray[currentSeq_i].ODSensor;
    ODTarget =  sequenceArray[currentSeq_i].ODTarget;
    ODDrift =  sequenceArray[currentSeq_i].ODDrift;
    next = sequenceArray[currentSeq_i].next;

    seqStartTime = millis();
    initialTemp = temp;
    initialOD1 = OD1;
    initialOD2 = OD2;
    initialOD3 = OD3;
    initialOD4 = OD4;
    initialOD5 = OD5;
    initialOD6 = OD6;
  }
}

void SequenceHandler::initiateSequence(float temp, float OD1, float OD2, float OD3, float OD4, float OD5, float OD6) {
  tempTarget =  sequenceArray[currentSeq_i].tempTarget;
  ODSensor =  sequenceArray[currentSeq_i].ODSensor;
  ODTarget =  sequenceArray[currentSeq_i].ODTarget;
  ODDrift =  sequenceArray[currentSeq_i].ODDrift;
  next = sequenceArray[currentSeq_i].next;

  seqStartTime = millis();
  initialTemp = temp;
  initialOD1 = OD1;
  initialOD2 = OD2;
  initialOD3 = OD3;
  initialOD4 = OD4;
  initialOD5 = OD5;
  initialOD6 = OD6;
}
