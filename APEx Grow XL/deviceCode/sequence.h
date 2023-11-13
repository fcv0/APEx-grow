#include "config.h"

class Sequence {
  public:
    Sequence(byte data[], int arraySize);
    Sequence();
    unsigned long combineBytesToLong(byte byte1, byte byte2, byte byte3, byte byte4);    

    int num;
    unsigned long timeTrigger;    
    float tempTrigger;
    float OD1Trigger;
    float OD2Trigger;
    float OD3Trigger;
    float OD4Trigger;
    float OD5Trigger;
    float OD6Trigger;
    float tempTarget;
    int ODSensor;
    float ODTarget;
    float ODDrift;
    int next;      
  
};

class SequenceHandler {
  public:
    SequenceHandler(byte data[], int arraySize, int seqLen); 
    SequenceHandler(); 
    void addSequence(byte data[], int arraySize); 
    void updateCurrentSequence(float temp, float OD1, float OD2, float OD3, float OD4, float OD5, float OD6);
    void initiateSequence(float temp, float OD1, float OD2, float OD3, float OD4, float OD5, float OD6);

    float tempTarget = 0;
    int ODSensor = 1;
    float ODTarget = 0;
    float ODDrift = 0;
    int next = 1;

    boolean newSequence = false;

    unsigned long seqTimeLeft = 0;
    
//  private:
    Sequence sequenceArray[40];
    int currentSeq_i = 0;
    int totalSequenceNumber;
    int sequenceEnd_i = 0;

    unsigned long seqStartTime = 0;
    float initialTemp = 0;
    float initialOD1 = 0;
    float initialOD2 = 0;
    float initialOD3 = 0;
    float initialOD4 = 0;
    float initialOD5 = 0;
    float initialOD6 = 0;       
};
