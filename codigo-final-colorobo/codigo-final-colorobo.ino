const int motor1PWM = 5;
const int motor1A = 3;
const int motor1B = 4;
const int motor2PWM = 10;
const int motor2A = 9;
const int motor2B = 8   ;

// Variables para almacenar el comando recibido desde Python
char command;

void setup() {
  // Configurar los pines como salidas
  pinMode(motor1PWM, OUTPUT);
  pinMode(motor1A, OUTPUT);
  pinMode(motor1B, OUTPUT);
  pinMode(motor2PWM, OUTPUT);
  pinMode(motor2A, OUTPUT);
  pinMode(motor2B, OUTPUT);

  // Iniciar la comunicación serial a 9600 bps
  Serial.begin(9600);
}

void loop() {
  // Leer el comando enviado desde Python
  if (Serial.available() > 0) {
    command = Serial.read();
    executeCommand(command);
  }
}

// Función para ejecutar el comando recibido desde Python
void executeCommand(char command) {
  switch (command) {
    case 'F': // Avanzar
      motorForward();
      break;
    case 'B': // Retroceder
      motorBackward();
      break;
    case 'L': // Girar a la izquierda
      motorLeft();
      break;
    case 'R': // Girar a la derecha
      motorRight();
      break;
    case 'S': // Detenerse
      motorStop();
      break;
    default:
      break;
  }
}

// Funciones para controlar los motores
void motorForward() {
  digitalWrite(motor1A, HIGH);
  digitalWrite(motor1B, LOW);
  analogWrite(motor1PWM, 255);
  
  digitalWrite(motor2A, HIGH);
  digitalWrite(motor2B, LOW);
  analogWrite(motor2PWM, 255);
}

void motorBackward() {
  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, HIGH);
  analogWrite(motor1PWM, 255);
  
  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, HIGH);
  analogWrite(motor2PWM, 255);
}

void motorLeft() {
   digitalWrite(motor1A, HIGH);
  digitalWrite(motor1B, LOW);
  analogWrite(motor1PWM, 100);
  
  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, HIGH);
  analogWrite(motor2PWM, 100);
}

void motorRight() {
  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, HIGH);
  analogWrite(motor1PWM, 100);
  
  digitalWrite(motor2A, HIGH);
  digitalWrite(motor2B, LOW);
  analogWrite(motor2PWM, 100);
}

void motorStop() {
  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, LOW);
  analogWrite(motor1PWM, 0);
  
  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, LOW);
  analogWrite(motor2PWM, 0);
}