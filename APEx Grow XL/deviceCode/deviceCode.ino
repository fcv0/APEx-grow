#include "pinMap.h"
#include "config.h"
#include "communications.h"
//#include "control.h"

#include <Adafruit_MLX90614.h>

#include <Wire.h>

Adafruit_MLX90614 mainIRSensor = Adafruit_MLX90614();
Adafruit_MLX90614 mediaIRSensor = Adafruit_MLX90614();

CommunicationHandler handler;
//TempController tempControl = TempController(0);
//ODController ODControl = ODController(0);

unsigned long curTime;
unsigned long lastComTime;
unsigned long runStart;

byte deviceStatus;

bool readingOD = false;
bool heatSet_OD;
bool ledActive = false;
unsigned long ledActivationTime;
int currentDiode = 0;

int ledPins [totalLEDs];
int diodeAddresses [totalLEDs];
int scatterRelationship [totalLEDs];
uint8_t diodeWires [totalLEDs];

bool readingODMedia = false;
bool heatSet_ODMedia;
bool ledActiveMedia = false;
unsigned long ledActivationTimeMedia;
int currentDiodeMedia = 0;

int ledPinsMedia [totalLEDsMedia];
int diodeAddressesMedia [totalLEDsMedia];
int scatterRelationshipMedia [totalLEDsMedia];
uint8_t diodeWiresMedia [totalLEDsMedia];

void setup() {
  Wire.begin();

  Serial.begin(9600);

  tcaselect(temp_sensor_wire);
  
  mainIRSensor.begin();
  delay(100);

  tcaselect(temp_sensor_wire_media);

  mediaIRSensor.begin();
  delay(100);

  tcaselect(diode1_wire);
  initialise_photodiode(diode1_addr);
  initialise_photodiode(diode2_addr);
  initialise_photodiode(diode3_addr);

  tcaselect(diode4_wire);
  initialise_photodiode(diode4_addr);
  initialise_photodiode(diode5_addr);
  initialise_photodiode(diode6_addr);

  tcaselect(diode1_wire_media);
  initialise_photodiode(diode1_addr);
  initialise_photodiode(diode2_addr);
  initialise_photodiode(diode3_addr);

  tcaselect(diode4_wire_media);
  initialise_photodiode(diode4_addr);
  initialise_photodiode(diode5_addr);
  initialise_photodiode(diode6_addr);

  curTime = millis();

  //pmw pumps
  pinMode(pump1SpeedPin, OUTPUT);//pump speed1
  pinMode(pump2SpeedPin, OUTPUT); //pump speed2
  pinMode(pump3SpeedPin, OUTPUT);//pump speed3
  pinMode(pump4SpeedPin, OUTPUT); //pump speed4
  pinMode(pump5SpeedPin, OUTPUT);//pump speed5
  pinMode(pump6SpeedPin, OUTPUT);//pump speed5

  pinMode(fanSpeedPin, OUTPUT); //fan speed
  pinMode(fan2SpeedPin, OUTPUT); //fan speed


  //digital pins
  pinMode(heaterPin , OUTPUT); //heater
  pinMode(heaterPinMedia , OUTPUT); //heater

  pinMode(pump1DirPin2 , OUTPUT); //pump1 onoff
  pinMode(pump2OnOffPin , OUTPUT); //pump2 onoff
  pinMode(pump3OnOffPin , OUTPUT); //pump3 onoff
  pinMode(pump4DirPin2 , OUTPUT); //pump4 onoff
  pinMode(pump5OnOffPin , OUTPUT); //pump5 onoff

  pinMode(pump1DirPin , OUTPUT); //pump1 dir
  pinMode(pump2DirPin , OUTPUT); //pump2 dir
  pinMode(pump3DirPin , OUTPUT); //pump3 dir
  pinMode(pump4DirPin , OUTPUT); //pump4 dir
  pinMode(pump5DirPin , OUTPUT); //pump5 dir

//  digitalWrite(pump1DirPin, HIGH);
//  digitalWrite(pump2DirPin, HIGH);
//  digitalWrite(pump3DirPin, HIGH);
//  digitalWrite(pump4DirPin, HIGH);
//  digitalWrite(pump5DirPin, HIGH);

  pinMode(led1Pin, OUTPUT); //led 1     for the OD sensor
  pinMode(led2Pin, OUTPUT); // led2
  pinMode(led3Pin, OUTPUT); // led 3
  pinMode(led4Pin, OUTPUT); // led 4
  pinMode(led5Pin, OUTPUT); // led5
  pinMode(led6Pin, OUTPUT); // led 6

  pinMode(led1PinMedia, OUTPUT); //led 1     for the OD sensor on the media chamber
  pinMode(led2PinMedia, OUTPUT); // led2
  pinMode(led3PinMedia, OUTPUT); // led 3
  pinMode(led4PinMedia, OUTPUT); // led 4
  pinMode(led5PinMedia, OUTPUT); // led5
  pinMode(led6PinMedia, OUTPUT); // led 6

  handler = CommunicationHandler();

  handler.tempControl = TempController(0, heaterPin);
  handler.ODControl = ODController(20);

  handler.tempControlMedia = TempController(0, heaterPinMedia);

//  handler.tempControlFossil = TempController(4, peltierPin, true);

//  ledPins[0] = led1Pin;
//  ledPins[1] = led2Pin;
//  ledPins[2] = led3Pin;
//  ledPins[3] = led4Pin;
//  ledPins[4] = led5Pin;
//  ledPins[5] = led6Pin;

  ledPins[0] = led1Pin;
  ledPins[1] = led2Pin;
  ledPins[2] = led2Pin;
  ledPins[3] = led2Pin;
  ledPins[4] = led2Pin;
  ledPins[5] = led2Pin;

//  diodeAddresses[0] = diode1_addr;
//  diodeAddresses[1] = diode2_addr;
//  diodeAddresses[2] = diode3_addr;
//  diodeAddresses[3] = diode4_addr;
//  diodeAddresses[4] = diode5_addr;
//  diodeAddresses[5] = diode6_addr;

  diodeAddresses[0] = diode2_addr;
  diodeAddresses[1] = diode2_addr;
  diodeAddresses[2] = diode1_addr;
  diodeAddresses[3] = diode3_addr;
  diodeAddresses[4] = diode5_addr;
  diodeAddresses[5] = diode6_addr;

  diodeWires[0] = diode1_wire;
  diodeWires[1] = diode2_wire;
  diodeWires[2] = diode3_wire;
  diodeWires[3] = diode4_wire;
  diodeWires[4] = diode5_wire;
  diodeWires[5] = diode6_wire;

//  scatterRelationship[0] = 3;
//  scatterRelationship[1] = 4;
//  scatterRelationship[2] = 5;
//  scatterRelationship[3] = 0;
//  scatterRelationship[4] = 1;
//  scatterRelationship[5] = 2;

  scatterRelationship[0] = 2;
  scatterRelationship[1] = 3;
  scatterRelationship[2] = 6;
  scatterRelationship[3] = 0;
  scatterRelationship[4] = 1;
  scatterRelationship[5] = 2;

//  ledPinsMedia[0] = led1PinMedia;
//  ledPinsMedia[1] = led2PinMedia;
//  ledPinsMedia[2] = led3PinMedia;
//  ledPinsMedia[3] = led4PinMedia;
//  ledPinsMedia[4] = led5PinMedia;
//  ledPinsMedia[5] = led6PinMedia;

  ledPinsMedia[0] = led2PinMedia;
  ledPinsMedia[1] = led2PinMedia;
  ledPinsMedia[2] = led2PinMedia;
  ledPinsMedia[3] = led2PinMedia;
  ledPinsMedia[4] = led2PinMedia;
  ledPinsMedia[5] = led2PinMedia;

//  diodeAddressesMedia[0] = diode1_addr;
//  diodeAddressesMedia[1] = diode2_addr;
//  diodeAddressesMedia[2] = diode3_addr;
//  diodeAddressesMedia[3] = diode4_addr;
//  diodeAddressesMedia[4] = diode5_addr;
//  diodeAddressesMedia[5] = diode6_addr;

  diodeAddressesMedia[0] = diode2_addr;
  diodeAddressesMedia[1] = diode2_addr;
  diodeAddressesMedia[2] = diode1_addr;
  diodeAddressesMedia[3] = diode3_addr;
  diodeAddressesMedia[4] = diode5_addr;
  diodeAddressesMedia[5] = diode6_addr;

  diodeWiresMedia[0] = diode1_wire_media;
  diodeWiresMedia[1] = diode2_wire_media;
  diodeWiresMedia[2] = diode3_wire_media;
  diodeWiresMedia[3] = diode4_wire_media;
  diodeWiresMedia[4] = diode5_wire_media;
  diodeWiresMedia[5] = diode6_wire_media;

//  scatterRelationshipMedia[0] = 3;
//  scatterRelationshipMedia[1] = 4;
//  scatterRelationshipMedia[2] = 5;
//  scatterRelationshipMedia[3] = 0;
//  scatterRelationshipMedia[4] = 1;
//  scatterRelationshipMedia[5] = 2;

  scatterRelationshipMedia[0] = 2;
  scatterRelationshipMedia[1] = 3;
  scatterRelationshipMedia[2] = 5;
  scatterRelationshipMedia[3] = 0;
  scatterRelationshipMedia[4] = 1;
  scatterRelationshipMedia[5] = 2;

//  pinMode(13, OUTPUT);

//  handler.fossilRecord = GantryController(250, 200, 150, 0.08, 8, 9, 10, 11, 7,
//                                          250, 200, 150, 0.08, 3, 4, 5, 6, 2);
}

void loop() {
  curTime = millis();
  handler.pumpController.updatePumps();

  if(handler.pumpController.speedsChanged){
    handler.addToStdBuffer(10);
  }

  handler.cycle();

  if(handler.refillCuvettes && !readingOD && !readingODMedia && !handler.pumpController.dilutionFlag && !handler.pumpController.speedsChanged && (millis() - handler.lastCuvetteRefillTime > handler.cuvetteRefillInterval)){
    handler.pumpController.cycleSensors();
    handler.lastCuvetteRefillTime = millis();
  }

  if(handler.reReferanceOD){
    referanceOD();
  }

  if(handler.reReferanceODMedia){
    referanceODMedia();
  }

  if (handler.runStartFlag) {
    handler.pumpController.setPumpSpeed(7, 50, false);
    handler.pumpController.setPumpSpeed(8, 50, false);
    handler.pumpController.setPumpSpeed(3, cuvettePumpSpeed, false);
    handler.pumpController.setPumpSpeed(0, cuvettePumpSpeed, false);
    handler.enableODSensing = true;
    handler.enableTempSensing = true;
    handler.enableODControl = true;
    handler.enableTempControl = true;
    handler.runInProgress = true;
    readTempSensors();
    readODSensors();

    handler.sequenceHandler.initiateSequence(handler.curTempIR, handler.ODs[0], handler.ODs[1], handler.ODs[2], handler.ODs[3], handler.ODs[4], handler.ODs[5] );
    handler.tempControl.setTarget(handler.sequenceHandler.tempTarget);
    handler.tempControlMedia.setTarget(handler.sequenceHandler.tempTarget);
    handler.ODControl.setTarget(handler.sequenceHandler.ODTarget, handler.sequenceHandler.ODDrift);

    handler.runStartFlag = false;
  }

  if (handler.runStopFlag) {     // add transmission of ending
    handler.addToPriorityBuffer(3);
    handler.enableODSensing = false;
    handler.enableTempSensing = true;
    handler.enableODControl = false;
    handler.enableTempControl = false;
    handler.tempControl.setTarget(0);
    handler.tempControlMedia.setTarget(0);
    handler.tempControl.heaterPower = 0;
    handler.tempControl.setHeaterPower();
    handler.runInProgress = false;

    handler.runStopFlag = false;
//    handler.pumpController.setPumpSpeed(3, 0, false);
  }

  if (handler.enableODSensing && millis() - handler.lastODSample > handler.ODSamplingInterval && !readingOD) {
    if (handler.pumpController.pumpSpeeds[3] != cuvettePumpSpeed){
      handler.pumpController.setPumpSpeed(3, cuvettePumpSpeed, false);
    }
    if (handler.pumpController.pumpSpeeds[0] != cuvettePumpSpeed){
      handler.pumpController.setPumpSpeed(0, cuvettePumpSpeed, false);
    }
    readODSensors();
//    if (handler.enableODControl) {
//      handler.ODControl.updateOutput(handler.ODs[handler.sequenceHandler.ODSensor]);
//      
//    }
  }
  if (readingOD) {
    readODSensors();
    if (!readingOD && handler.enableODControl) {
      handler.ODControl.updateOutput(handler.ODs[handler.sequenceHandler.ODSensor]);
      if(!handler.pumpController.dilutionFlag && handler.ODControl.pumpPower != 0){
        handler.pumpController.dilute(handler.ODControl.pumpPower);
      }
    }
  }

  if (handler.enableODSensing && millis() - handler.lastODSampleMedia > handler.ODSamplingIntervalMedia && !readingODMedia) {
    readODSensorsMedia();
  }
  if (readingODMedia) {
    readODSensorsMedia();
  }
  
  
  if (handler.enableTempSensing && millis() - handler.lastTempSample > handler.tempSamplingInterval) {
    readTempSensors();
    if (handler.enableTempControl) {
      handler.tempControl.updateOutput(handler.curTempIR);
    }
  }

  if (handler.enableTempSensing && millis() - handler.lastTempSampleMedia > handler.tempSamplingIntervalMedia) {
    readTempSensorsMedia();
    if (handler.enableTempControl) {
      handler.tempControlMedia.updateOutput(handler.curTempIRMedia);
    }
  }


  if (handler.runInProgress ) { // && (handler.newTempToSend || handler.newODToSend)
    handler.sequenceHandler.updateCurrentSequence(handler.curTempIR, handler.ODs[0], handler.ODs[1], handler.ODs[2], handler.ODs[3], handler.ODs[4], handler.ODs[5] );
    if (handler.sequenceHandler.newSequence) {
      handler.ODControl.setTarget(handler.sequenceHandler.ODTarget, handler.sequenceHandler.ODDrift);
      handler.tempControl.setTarget(handler.sequenceHandler.tempTarget);
      handler.tempControlMedia.setTarget(handler.sequenceHandler.tempTarget);
      if (handler.sequenceHandler.next == 0) {
        handler.runStopFlag = true;
      }
    }
  }
}

void readTempSensors() {
  bool heatSet = handler.tempControl.heaterPowerSet == 255;
//  digitalWrite(heaterPin, LOW);
//  delay(tempSensorDelay);
  int temp_int = analogRead(temperaturePin);
  handler.curTempRawHeaterPower = handler.tempControl.heaterPower;
  handler.curTempRawHeaterPowerSet = heatSet * 255;
  handler.curTempRaw = temp_int;
  handler.curTemp = float(temp_int) * handler.tempCalibrationGradient + handler.tempCalibraitonOffset; // * 0.2195 - 62.282; //* handler.tempCalibrationGradient + handler.tempCalibraitonOffset;// try using float(temp_int)
//  digitalWrite(heaterPin, heatSet);
  
  tcaselect(temp_sensor_wire);

  handler.curTempIR = mainIRSensor.readObjectTempC();
  handler.curAmbientTempIR = mainIRSensor.readAmbientTempC();

  handler.lastTempSample = millis();
  handler.addToStdBuffer(6);
  handler.newTempToSend = true;
}

void readTempSensorsMedia() {
  bool heatSet = handler.tempControl.heaterPowerSet == 255;
//  digitalWrite(heaterPin, LOW);
//  delay(tempSensorDelay);
  int temp_int = analogRead(temperaturePinMedia);
  handler.curTempRawHeaterPowerMedia = handler.tempControl.heaterPower;
  handler.curTempRawHeaterPowerSetMedia = heatSet * 255;
  handler.curTempRawMedia = temp_int;
  handler.curTempMedia = float(temp_int) * handler.tempCalibrationGradient + handler.tempCalibraitonOffset; // * 0.2195 - 62.282; //* handler.tempCalibrationGradient + handler.tempCalibraitonOffset;// try using float(temp_int)
//  digitalWrite(heaterPin, heatSet);

  tcaselect(temp_sensor_wire_media);

  handler.curTempIRMedia = mediaIRSensor.readObjectTempC();
  handler.curAmbientTempIRMedia = mediaIRSensor.readAmbientTempC();

  handler.lastTempSampleMedia = millis();
  handler.addToStdBuffer(9);
  handler.newTempToSendMedia = true;
}

void readODSensors() {
  if (readingODMedia){
    return;
  }
  if (!readingOD) {
//    heatSet_OD = handler.tempControl.heaterPowerSet == 255;
//    digitalWrite(heaterPin, LOW);
    handler.lastODSample = millis();
    readingOD = true;
  }

  if (handler.ODsToRead[currentDiode]) {
    if (!ledActive) {
      digitalWrite(ledPins[currentDiode], HIGH);
      ledActive = true;
      ledActivationTime = millis();
      read_photodiode(diodeAddresses[currentDiode], diodeWires[currentDiode]); //read absorbtion
      read_photodiode(diodeAddresses[scatterRelationship[currentDiode]], diodeWires[scatterRelationship[currentDiode]]); //read scatter
    } else if (millis() - ledActivationTime > ODSensorDelay) {
      ledActive = false;
      handler.absorb[currentDiode] = read_photodiode(diodeAddresses[currentDiode], diodeWires[currentDiode]); //read absorbtion
      handler.scatter[currentDiode] = read_photodiode(diodeAddresses[scatterRelationship[currentDiode]], diodeWires[scatterRelationship[currentDiode]]); //read scatter
      digitalWrite(ledPins[currentDiode], LOW);
      currentDiode ++;      
    }
  }else{
    currentDiode ++;
  }
  if (currentDiode == totalLEDs) {
//    digitalWrite(heaterPin, heatSet_OD);
    generateODs();
    currentDiode = 0;
    readingOD = false;
    handler.newODToSend = true;
    handler.addToStdBuffer(4);
    handler.addToStdBuffer(5);
  }
}

void generateODs() {  
  for (int i = 0; i < totalLEDs; i++) {
    if (handler.absorb[i] < 100000) {
      handler.ODs[i] = 0;
      handler.rawODs[i] = 0;
    } else {
      handler.rawODs[i] = -log10(handler.absorb[i] / handler.ODReferenceAbsorbance[i]);
      handler.ODs[i] = handler.rawODs[i] * handler.ODCalibrationGradient + handler.ODCalibraitonOffset;
    }
  }
}

void readODSensorsMedia() {
  if (readingOD){
    return;
  }
  if (!readingODMedia) {
//    heatSet_OD = handler.tempControl.heaterPowerSet == 255;
//    digitalWrite(heaterPin, LOW);
    handler.lastODSampleMedia = millis();
    readingODMedia = true;
  }

  if (handler.ODsToReadMedia[currentDiodeMedia]) {
    if (!ledActiveMedia) {
      digitalWrite(ledPinsMedia[currentDiodeMedia], HIGH);
      ledActiveMedia = true;
      ledActivationTimeMedia = millis();
      read_photodiode(diodeAddressesMedia[currentDiodeMedia], diodeWiresMedia[currentDiodeMedia]); //read absorbtion
      read_photodiode(diodeAddressesMedia[scatterRelationshipMedia[currentDiodeMedia]], diodeWiresMedia[scatterRelationshipMedia[currentDiodeMedia]]); //read scatter
    } else if (millis() - ledActivationTimeMedia > ODSensorDelay) {
      ledActiveMedia = false;
      handler.absorbMedia[currentDiodeMedia] = read_photodiode(diodeAddressesMedia[currentDiodeMedia], diodeWiresMedia[currentDiodeMedia]); //read absorbtion
      handler.scatterMedia[currentDiodeMedia] = read_photodiode(diodeAddressesMedia[scatterRelationshipMedia[currentDiodeMedia]], diodeWiresMedia[scatterRelationshipMedia[currentDiodeMedia]]); //read scatter
      digitalWrite(ledPinsMedia[currentDiodeMedia], LOW);
      currentDiodeMedia ++;      
      }
    }else{
      currentDiodeMedia ++;
    }
    if (currentDiodeMedia == totalLEDsMedia) {
//      digitalWrite(heaterPin, heatSet_OD);
      generateODsMedia();
      currentDiodeMedia = 0;
      readingODMedia = false;
      handler.newODToSendMedia = true;
      handler.addToStdBuffer(7);
      handler.addToStdBuffer(8);
  }
}

void generateODsMedia() {  
  for (int i = 0; i < totalLEDsMedia; i++) {
    if(!handler.ODsToReadMedia[i]){
      handler.ODsMedia[i] = 0;
      handler.rawODsMedia[i] = 0;
    }
    else if (handler.absorbMedia[i] < 100000) {
      handler.ODsMedia[i] = 0;
      handler.rawODsMedia[i] = 0;
    } else {
      handler.rawODsMedia[i] = -log10(handler.absorbMedia[i] / handler.ODReferenceAbsorbanceMedia[i]);
      handler.ODsMedia[i] = handler.rawODsMedia[i] * handler.ODCalibrationGradient + handler.ODCalibraitonOffset;
    }
  }
}

void readAllSensors() {
  readTempSensors();
  readODSensors();
}

void referanceOD(){
  for(int i = 0; i < 6; i++){
    if(handler.ODsToRead[i]){
      handler.ODReferenceAbsorbance[i] = handler.absorb[i];
    }else{
      handler.ODReferenceAbsorbance[i] = 3300000;
    }
  }
  handler.reReferanceOD = false;
  handler.addToStdBuffer(68);
}

void referanceODMedia(){
  for(int i = 0; i < 6; i++){
    if(handler.ODsToReadMedia[i]){
      handler.ODReferenceAbsorbanceMedia[i] = handler.absorbMedia[i];
    }else{
      handler.ODReferenceAbsorbanceMedia[i] = 3300000;
    }
  }
  handler.reReferanceODMedia = false;
  handler.addToStdBuffer(69);
}


void initialise_photodiode(int device_address) {
  byte d1;
  byte d2;
  Wire.beginTransmission(device_address);
  Wire.write(config_reg);
  Wire.endTransmission();

  Wire.requestFrom(device_address, 2, true);

  if (Wire.available() >= 2) {
    d1 = Wire.read();
    d2 = Wire.read();
  }
  d1 = d1 | 0b00000110;

  Wire.beginTransmission(device_address);
  Wire.write(config_reg);
  Wire.write(d1);
  Wire.write(d2);
  Wire.endTransmission();
}

float read_photodiode(int device_address, uint8_t wire) {
  tcaselect(wire);

  uint16_t d = 0;
  byte d1;
  byte d2;
  Wire.beginTransmission(device_address);
  Wire.write(result_reg);
  Wire.endTransmission();

  Wire.requestFrom(device_address, 2, true);

  if (Wire.available() >= 2) {
    d1 = Wire.read();
    d2 = Wire.read();
    d = ((d1 << 8) | d2);
  }
  float internal_spec_resp_fac = 0.4;
  float optical_power = (d & 0b0000111111111111) * pow(2.0, ((d & 0b1111000000000000)) >> 12) * 1.2 / internal_spec_resp_fac;
  return optical_power;

}

void tcaselect(uint8_t i) {
  if (i > 7) return;

  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
}
