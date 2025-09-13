#include <WiFi.h>
#include <ESP_Mail_Client.h>

// Wi-Fi Credentials
const char* ssid = "";
const char* password = "";

// Gmail Configuration
#define SMTP_HOST "smtp.gmail.com"
#define SMTP_PORT 465
#define SENDER_EMAIL "ragul2210673@ssn.edu.in"
#define SENDER_PASSWORD "khpofykxdkgjzgpa"
#define RECIPIENT_EMAIL "ragul2210673@ssn.edu.in"

// Ultrasonic Sensor Pins
#define TRIG1 12
#define ECHO1 13
#define TRIG2 14
#define ECHO2 15
#define TRIG3 16
#define ECHO3 17
#define TRIG4 18
#define ECHO4 19

// Control
#define STOP_BUTTON 0        // GPIO0 (BOOT)
#define CHECK_INTERVAL 5000  // 5 seconds
#define FULL_DISTANCE 10     // 10cm threshold

SMTPSession smtp;
volatile bool systemActive = true;

void IRAM_ATTR stopSystem() {
  systemActive = !systemActive;
  Serial.println(systemActive ? "\nSYSTEM RESUMED" : "\nSYSTEM PAUSED");
}

void setup() {
  Serial.begin(115200);

  // Configure Hardware
  pinMode(STOP_BUTTON, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(STOP_BUTTON), stopSystem, FALLING);

  // Ultrasonic Pins
  pinMode(TRIG1, OUTPUT);
  pinMode(ECHO1, INPUT);
  pinMode(TRIG2, OUTPUT);
  pinMode(ECHO2, INPUT);
  pinMode(TRIG3, OUTPUT);
  pinMode(ECHO3, INPUT);
  pinMode(TRIG4, OUTPUT);
  pinMode(ECHO4, INPUT);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nConnected!");
}

float readDistance(uint8_t trig, uint8_t echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  return pulseIn(echo, HIGH) * 0.0343 / 2;
}

void sendAlert(String binDetails) {
  Session_Config config;
  config.server.host_name = SMTP_HOST;
  config.server.port = SMTP_PORT;
  config.login.email = SENDER_EMAIL;
  config.login.password = SENDER_PASSWORD;

  SMTP_Message message;
  message.sender.name = "Bin Monitor";
  message.sender.email = SENDER_EMAIL;
  message.subject = "[ALERT] Bins Full!";
  message.addRecipient("Maintenance", RECIPIENT_EMAIL);
  message.text.content = "Full Bins:\n" + binDetails;

  if (smtp.connect(&config)) {
    MailClient.sendMail(&smtp, &message);
    smtp.closeSession();
  }
}

void loop() {
  if (!systemActive) {
    delay(1000);
    return;
  }

  // Read all bins
  float d1 = readDistance(TRIG1, ECHO1);
  float d2 = readDistance(TRIG2, ECHO2);
  float d3 = readDistance(TRIG3, ECHO3);
  float d4 = readDistance(TRIG4, ECHO4);

  // Serial Monitor Output
  Serial.printf("Bin1: %.1fcm | Bin2: %.1fcm | Bin3: %.1fcm | Bin4: %.1fcm\n",
                d1, d2, d3, d4);

  // Check for full bins
  String fullBins = "";
  if (d1 < FULL_DISTANCE) fullBins += "Bin1, ";
  if (d2 < FULL_DISTANCE) fullBins += "Bin2, ";
  if (d3 < FULL_DISTANCE) fullBins += "Bin3, ";
  if (d4 < FULL_DISTANCE) fullBins += "Bin4, ";

  // Send alert if any bins full
  if (fullBins.length() > 0) {
    fullBins.remove(fullBins.length() - 2);  // Remove last comma
    sendAlert(fullBins);
    Serial.println("Alert sent: " + fullBins);
  }

  delay(CHECK_INTERVAL);
}