// Arduino: LED control via Serial from ROS2
const int LED_PIN = 13;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  digitalWrite(LED_PIN, LOW);
  Serial.println("Arduino Ready!");
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == '1') {
      digitalWrite(LED_PIN, HIGH);   // LED ON
      Serial.println("LED ON");
    } else if (cmd == '0') {
      digitalWrite(LED_PIN, LOW);    // LED OFF
      Serial.println("LED OFF");
    }
  }
}
