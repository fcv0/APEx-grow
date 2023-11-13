
#define dudPin 0

//pwm pins

#define pump1SpeedPin 7        // media OD sensor
#define pump2SpeedPin 9        // fresh media/ dh20 into media chamber
#define pump3SpeedPin 11        // media chamber into main chamber
#define pump4SpeedPin 6        // OD sensor
#define pump5SpeedPin 10        // waste
#define pump6SpeedPin 8        // bleach / ethanol into media chameber (or main if media not conneced
#define pump7SpeedPin 0        // fossil record

#define fanSpeedPin 3          // main chamber
#define fan2SpeedPin 2        // media chamber


//digital pins
#define heaterPin 53
#define heaterPinMedia 52
#define peltierPin 0

#define pump1DirPin 32
#define pump1DirPin2 33
#define pump2DirPin 41
#define pump2OnOffPin 40
#define pump3DirPin 35
#define pump3OnOffPin 34
#define pump4DirPin 31
#define pump4DirPin2 30
#define pump5DirPin 37
#define pump5OnOffPin 36
#define pump6DirPin 39
#define pump6OnOffPin 38
#define pump7DirPin 0
#define pump7OnOffPin 0

#define led1Pin 23
#define led2Pin 23
#define led3Pin 23
#define led4Pin 23
#define led5Pin 23
#define led6Pin 23

#define led1PinMedia 22
#define led2PinMedia 22
#define led3PinMedia 22
#define led4PinMedia 22
#define led5PinMedia 22
#define led6PinMedia 22

//analog pins
#define temperaturePin A0
#define temperaturePinMedia A1

// address map
#define TCAADDR 0x70

#define diode1_addr 0x44
#define diode1_wire 0
#define diode2_addr 0x45
#define diode2_wire 0
#define diode3_addr 0x47
#define diode3_wire 0

#define diode4_addr 0x44
#define diode4_wire 0
#define diode5_addr 0x45
#define diode5_wire 0
#define diode6_addr 0x47
#define diode6_wire 0

#define diode1_wire_media 1
#define diode2_wire_media 1
#define diode3_wire_media 1

#define diode4_wire_media 1
#define diode5_wire_media 1
#define diode6_wire_media 1

#define result_reg 0x00
#define config_reg 0x01

#define temp_sensor_wire 7
#define temp_sensor_wire_media 5


// fossil record
//#define limitPinX 7
//#define limitPinY 2
//
//#define stepperXPin1 8
//#define stepperXPin2 9
//#define stepperXPin3 10
//#define stepperXPin4 11
//
//#define stepperYPin1 3
//#define stepperYPin2 4
//#define stepperYPin3 5
//#define stepperYPin4 6
