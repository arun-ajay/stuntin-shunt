//Note APDS Library Written by Davide Depau: https://github.com/Depau/APDS9930

#include <Wire.h>
#include <APDS9930.h>
#include <SoftwareSerial.h>
#define RxD 0
#define TxD 1
/*PROXIMITY SENSOR DEFINITIONS/VARIABLES********************************************/
// Pins
#define APDS9930_INT    2  // Needs to be an interrupt pin

// Constants
#define PROX_INT_HIGH   0 // Proximity level for interrupt, minimum value
#define PROX_INT_LOW    0  // Absolute minimum

// Global variables
APDS9930 apds = APDS9930(); //module object from custom library
uint16_t proximity_data = 0; //float data
volatile bool isr_flag = false; //interrupt, cyclable from True to False in loop

//Flag
int prox_flag = 1;
/************************************************************************************/
/*FORCE SENSITIVE RESISTOR DEFINITIONS/VARIABLES*************************************/
//Pins 
const int fsrAnalogPin = A0;
int fsrReading;

//Flag
int fsr_flag = 0;

/************************************************************************************/
SoftwareSerial BTSerial(RxD,TxD);

void setup() {
  // Initialize Serial port
  BTSerial.begin(9600);
/*PROXIMITY SENSOR INITIALIZATIONS********************************************/
  pinMode(APDS9930_INT, INPUT);
  

  
  // Initialize interrupt service routine
  attachInterrupt(0, interruptRoutine, FALLING);
  
  // Initialize APDS-9930 (configure I2C and initial values)
  apds.init();
  
  // Adjust the Proximity sensor gain
  apds.setProximityGain(PGAIN_1X);
  
  // Set proximity interrupt thresholds
  apds.setProximityIntLowThreshold(PROX_INT_LOW);
  apds.setProximityIntHighThreshold(PROX_INT_HIGH);
  
  // Start running the APDS-9930 proximity sensor (interrupts)
  apds.enableProximitySensor(true);
/************************************************************************************/
/*FSR INITIALIZATIONS NOT NEEDED*****************************************************/
}

void loop() {

/*PROXIMITY SENSOR SERIAL PRINT LOOP*************************************************/
  // If interrupt occurs, print out the proximity level
  //Flag: 1 ->Flow detected, 0 -> Flow not detected

  if ( isr_flag ) {
    
    // Read proximity level and print it out
    if (apds.readProximity(proximity_data)){
      if(proximity_data > 600 && prox_flag == 0)
      {
        BTSerial.print("Flow detected! Level: ");
        BTSerial.println(proximity_data);
        prox_flag = 1;
      }
      if(proximity_data <=600 && prox_flag == 1)
      {
        BTSerial.print("No Flow detected! Level: ");
        BTSerial.println(proximity_data);
        prox_flag = 0;
      }
    //delay(500);
      
    }
    // Reset flag and clear APDS-9930 interrupt (IMPORTANT!)
    isr_flag = false;
    apds.clearProximityInt();
    
  }
/**************************************************************************************/

/*FSR SERIAL SERIAL PRINT LOOP*********************************************************/
  fsrReading = analogRead(fsrAnalogPin);
  int num = fsrReading/3;
  //Flag: 1 ->Diaphragm open, 0 -> Flow diaphragm closed

  
  if (num >250 && fsr_flag == 1)
  {
    BTSerial.print("Diaphragm Closed. FSR Reading = ");
    BTSerial.println(num);
    fsr_flag = 0;
  }
  if (num <100 && fsr_flag == 0)
  {
      BTSerial.print("Diaphragm Open. FSR Reading = ");
      BTSerial.println(num);
      fsr_flag = 1;
   }
  delay(100);
/**************************************************************************************/

}

void interruptRoutine() {
  isr_flag = true;
}
