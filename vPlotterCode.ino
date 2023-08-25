#include <Servo.h>

#include <AccelStepper.h>
#include <AFMotor.h>

#define STEPS_PER_REVOLUTION = 200
#define STEP_SIZE = 1.8

// paramettre pour servo moteur
Servo pen_servo;
const int PEN_DOWN_POS = 175;
const int PEN_UP_POS = 0;


// position de moteur et nbr de step par revolution
AF_Stepper motor1(200, 1);
AF_Stepper motor2(200, 2);

void forwardstep1() {  
  motor1.onestep(FORWARD, SINGLE);
}
void backwardstep1() {  
  motor1.onestep(BACKWARD, SINGLE);
}
// wrappers for the second motor!
void forwardstep2() {  
  motor2.onestep(FORWARD, SINGLE);
}
void backwardstep2() {  
  motor2.onestep(BACKWARD, SINGLE);
}

AccelStepper stepper1(forwardstep1, backwardstep1);
AccelStepper stepper2(forwardstep2, backwardstep2);


long last_active_at = millis();
long deltas[2]; //tableu pour x et y en deplacement

// pormettre au servo de tourner vers le bas
void penDown() {
  pen_servo.write(PEN_DOWN_POS);
  delay(15);
}

// pormettre au servo de tourner vers le haut
void penUp() {
  pen_servo.write(PEN_UP_POS);
  last_active_at = millis();
}

int readByte() {
 // on attends qu'on recoi un byte on le lit puis on le renvoi
  while (Serial.available() == 0);
  return Serial.read();
}

void setup() {
 
  Serial.begin(9600);
 
  penUp();
}

void loop() {
  // lecture de byte envoye par le controlleur
  int incomingByte = readByte();

  switch (incomingByte) {
    case 'p': // commande pour servo
      // lecture de deuxieme byte 
      incomingByte = readByte();

      if (incomingByte == 'u') {
        penUp();
        Serial.print(COMMAND_COMPLETE_BYTE);
      } else if (incomingByte == 'd') {
        penDown();
        Serial.print(COMMAND_COMPLETE_BYTE);
      } else {
        Serial.print("Second byte ('");
        Serial.write(incomingByte); // Use write for sending single bytes
        Serial.println("') of up/down command is invalid");
      }
      break;
    case 'm': // commande pour moteur
      deltas[0] = Serial.parseInt();
      deltas[1] = Serial.parseInt();
      stepper.move(deltas[0]);  // Déplacer de 200 pas dans le sens des aiguilles d'une montre
      stepper.runToPosition();
      stepper.move(deltas[1]);  // Déplacer de 200 pas dans le sens des aiguilles d'une montre
      stepper.runToPosition();
      break;
    default:
      Serial.write(incomingByte); // Use write for sending single bytes
      break;
  }
  readByte(); //ignore the newline character

}
