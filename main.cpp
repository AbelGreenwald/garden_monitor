#include <mbed.h>
#include <math.h>

Serial xbee(D1, D0, 115200);
AnalogIn sen1(A0);
DigitalOut led(LED1);
DigitalOut sens_on(D2);
DigitalOut xbee_rst(D12);
LowPowerTicker toggleTicker;
bool sleep_now;
void toggle_led(void)
{
  led = !led;
  sleep_now = false;
}

int main() {
  xbee_rst = false;
  wait_ms(100);
  xbee_rst = true;
  float read1_norm;
  float read1_avg;
  toggleTicker.attach(toggle_led, 1);

  while (true) {
    sens_on = true;
    wait_ms(250);
    read1_avg = (sen1.read() + sen1.read() + sen1.read()) / 3;
    sens_on =  false;
    // Normalize .445 to .858, truncate noise
    read1_norm = (read1_avg - .445)/(.858 - .445);
    if (read1_norm <= 0){
      read1_norm = 0;
    }
    else if (read1_norm >= 1){
      read1_norm = 1;
    }
    xbee.printf("%f",ceil(read1_norm *100));
    xbee.putc('\n');
    wait(10);
  }
}
