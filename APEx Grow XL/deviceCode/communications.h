#include "sequence.h"
#include "control.h"
#include "gantry.h"

class CommunicationHandler {
  public:
    CommunicationHandler();

    PumpController2 pumpController = PumpController2();
    
    TempController tempControl = TempController(0, heaterPin);
    ODController ODControl = ODController(20);

    TempController tempControlMedia = TempController(0, heaterPinMedia);

    TempController tempControlFossil = TempController(100, peltierPin, true);

    boolean runStartFlag = false;
    boolean runStopFlag = false;

    boolean enableODSensing = true;
    boolean enableTempSensing = true;
    boolean enableODControl = true;
    boolean enableTempControl = true;

    float tempCalibrationGradient = 0.2195;
    float tempCalibraitonOffset = -62.282;
    unsigned long tempSamplingInterval = 3000;
    unsigned long lastTempSample = 0;
    int curTempRaw = 0;
    float curTemp = 0;
    float curTempIR = 0;
    float curAmbientTempIR = 0;
    int curTempRawHeaterPower = 0;
    int curTempRawHeaterPowerSet = 0;
    bool newTempToSend = false;

    unsigned long tempSamplingIntervalMedia = 3000;
    unsigned long lastTempSampleMedia = 0;
    int curTempRawMedia = 0;
    float curTempMedia = 0;
    float curTempIRMedia = 0;
    float curAmbientTempIRMedia = 0;
    int curTempRawHeaterPowerMedia = 0;
    int curTempRawHeaterPowerSetMedia = 0;
    bool newTempToSendMedia = false;

     //  handler.ODCalibrationGradient = 11.131;
    //  handler.ODCalibraitonOffset = - 0.277;
    float ODCalibrationGradient = 11.131*8/9.65 *0.915;
    float ODCalibraitonOffset = 0;
    float ODReferenceAbsorbance[6] = {5887483.982,5887483.982,5887483.982,5887483.982,5887483.982,5887483.982};
    unsigned long ODSamplingInterval = 15000;
    unsigned long lastODSample = 0;

    boolean ODsToRead[6] = {true, true, false, false, false, false};
    float absorb[6] = {1, 2, 3, 4, 5, 6};
    float scatter[6] = {0, 0, 0, 0, 0, 0};
    float ODs[6] = {1, 2, 3, 4, 5, 6};
    float rawODs[6] = {1, 2, 3, 4, 5, 6};
    bool newODToSend = false;

    float ODReferenceAbsorbanceMedia[6] = {5526524.026,5526524.026,5526524.026,5526524.026,5526524.026,5526524.026};
    unsigned long ODSamplingIntervalMedia = 30000;
    unsigned long lastODSampleMedia = 0;

    boolean ODsToReadMedia[6] = {true, true, false, false, false, false};
    float absorbMedia[6] = {1, 2, 3, 4, 5, 6};
    float scatterMedia[6] = {0, 0, 0, 0, 0, 0};
    float ODsMedia[6] = {1, 2, 3, 4, 5, 6};
    float rawODsMedia[6] = {1, 2, 3, 4, 5, 6};
    boolean newODToSendMedia = false;

    boolean refillCuvettes = true;
    unsigned long cuvetteRefillInterval = 600000; 
    unsigned long lastCuvetteRefillTime = 0; 

    boolean reReferanceOD = false;
    boolean reReferanceODMedia = false;
    
    boolean runInProgress = false;


    //connected modules
    boolean mediaPreHeaterConnected = false;
    boolean mediaPrepConnected = false;
    boolean sterilizationConnected = false;
    boolean fossilRecordConnected = false;

    void cycle();

    void addToStdBuffer(byte code);
    void addToPriorityBuffer(byte code);

    byte deviceStatus;
    byte PCStatus;

    unsigned long PCTime = 0;

    float p;
    float i;
    float d;

    

    int sequenceLength = 0;
    SequenceHandler sequenceHandler = SequenceHandler();


    // fossil record

    GantryController fossilRecord = GantryController();
    WellPlate wellPlate = WellPlate();

    int wellPlateRows = 4;
    int wellPlateColumns = 6;
    float wellPlateRowSpacing = 1.95;
    float wellPlateColumnSpacing = 1.95;

  private:
    boolean commsTurn = false;

    byte priorityOutBuffer[40] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    int priorityOutBuffer_i = 1;

    byte standardOutBuffer[40] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    int standardOutBuffer_i = 1;


    byte outbound[60] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    byte inbound[60] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

    void encodeOutbound();
    boolean validateInbound();
    void extractInbound();

    int combineBytesToInt(byte byte1, byte byte2);
    unsigned long combineBytesToLong(byte byte1, byte byte2, byte byte3, byte byte4);
    float combineBytesToFloat(byte byte1, byte byte2, byte byte3, byte byte4);
    void placeIntInOutbound(int val, int index1, int index2);
    void placeLongInOutbound(unsigned long val, int index1, int index2, int index3, int index4);
    void placeFloatInOutbound(float val, int index1, int index2, int index3, int index4);
    void flushInputBuffer();
    unsigned int fletcherChecksum(byte data[60], int count);

    float moveX;
    float moveY;
    boolean firstWellProvided = false;
    float firstWellX = 0;
    float firstWellY = 0;
    boolean lastWellProvided = false;
    float lastWellX = 0;
    float lastWellY = 0;
};
