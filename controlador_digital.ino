#include <String.h>
#include <Arduino.h>

#define ADC_OUTPUT_PIN 15
#define PWM_PIN 2
#define SAMPLE_TIME 50
#define MAX_BITS 4095
#define MAX_PWM_VALUE 4095
#define OFFSET_POTENTIOMETER 24
#define MAX_INPUT_ANGLE 90
#define MAX_OUTPUT_ANGLE 270

int current_time = 0, output_pot_value, pi_value, pwm_value;
unsigned long start_time = millis();
float e_1 = 0, u_1 = 0, input_angle = -1, output_angle;
String data_values;

uint16_t pi(float r, float y) {
  float e, u;
  e = r - y;
  u = u_1 + 0.016381*e + 0.016381 * e_1;

  if (u > MAX_INPUT_ANGLE)
    u = MAX_INPUT_ANGLE;
  else if (u < 0)
    u = 0;

  e_1 = e;
  u_1 = u;

  return uint32_t(u);
}

int convert_scale(uint16_t variable, uint16_t max_scale_1, uint16_t max_scale_2){
  return variable*max_scale_2/max_scale_1;
}


void setup() {
  Serial.begin(115200);
  pinMode(PWM_PIN, OUTPUT);
  ledcAttachPin(2, 0);
  ledcSetup(0, 1000, 12);
  input_angle = 0;
  Serial.setTimeout(1);
}

float time_s = 0;
void loop() {
  if(millis() - start_time > SAMPLE_TIME){

    start_time = millis();
    output_pot_value = analogRead(ADC_OUTPUT_PIN);
    output_angle = convert_scale(output_pot_value, MAX_BITS, MAX_OUTPUT_ANGLE) - OFFSET_POTENTIOMETER;
    pi_value = pi(input_angle, output_angle);
    pwm_value = convert_scale(pi_value, MAX_INPUT_ANGLE, MAX_PWM_VALUE);        
    if (Serial.available() > 0){
      input_angle = Serial.parseFloat();
    }
    if (input_angle == -1)
      pwm_value = 0;
    
    ledcWrite(0, pwm_value);
 
    data_values = String(String(start_time) + ',' + String(input_angle) + ',' + (output_angle) + ',' + String(pwm_value));
    Serial.println(data_values);
    time_s += 0.05;
    
  }

}
