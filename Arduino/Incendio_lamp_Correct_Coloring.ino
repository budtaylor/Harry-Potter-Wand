#include <Adafruit_NeoPixel.h>
#ifdef __AVR_ATtiny85__ // Trinket, Gemma, etc.
 #include <avr/power.h>
#endif

#define PIN 3

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(8, PIN);

uint8_t  mode   = 0, // Current animation effect
         offset = 0; // Position of spinny eyes
uint32_t color  = 0xc22404; // Start red
uint32_t prevTime;


void setup() {
  //start serial connection
  Serial.begin(9600);
  //configure pin2 as an input and enable the internal pull-up resistor
  pinMode(2, INPUT_PULLUP);
  //pinMode(13, OUTPUT);


#ifdef __AVR_ATtiny85__ // Trinket, Gemma, etc.
  if(F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif
  pixels.begin();
//  pixels.setBrightness(255); // 255 full brightness
  prevTime = millis();
}



void loop() {
  //read the pushbutton value into a variable
  int sensorVal = digitalRead(2);
  //print out the value of the pushbutton
  Serial.println(sensorVal);

  // Keep in mind the pullup means the pushbutton's
  // logic is inverted. It goes HIGH when it's open,
  // and LOW when it's pressed. Turn on pin 13 when the
  // button's pressed, and off when it's not:
  if (sensorVal == HIGH) {
   // digitalWrite(13, LOW);
    digitalWrite(12, LOW);

  } else {
  //  digitalWrite(13, HIGH);
   // delay (100);
    digitalWrite(12, HIGH);
    delay (200);



      uint8_t  i;
  uint32_t t;
  switch(mode) {

   case 0: // Random sparks - just one LED on at a time!
//    FIRE = 0xc24a04
    i = random(8);
    pixels.setPixelColor(i, color);
    pixels.setBrightness(170); // 255 full brightness
    pixels.show();
    delay(200);
    pixels.setPixelColor(i, 0xf38434); //set other color 0xBA2100,CB1500
    pixels.setBrightness(100); // 255 full brightness
    break;
 
   case 1: // Spinny wheels (8 LEDs on at a time)
    for(i=0; i<12; i++) {
      uint32_t c = 0xc24a04;  //set other color as yellow
      if(((offset + i) & 7) < 2) c = color; // 4 pixels on...
      pixels.setPixelColor(   i, c); // First eye
//      pixels.setPixelColor(2-i, c); // Second eye (flipped)
    }
    pixels.show();
    offset++;
    delay(30);
    break;
  }

  t = millis();
  if((t - prevTime) > 20000) {      // Every 20 seconds...
    mode++;                        // Next mode
    if(mode > 0) {                 // End of modes?
      mode = 0;                    // Start modes over
//      color >>= 8;                 // Next color R->G->B
//      if(!color) color = 0xFF0000; // Reset to red
    }
    for(i=0; i<12; i++) pixels.setPixelColor(i, 0);
    prevTime = t;
  
 
  }
  }}
