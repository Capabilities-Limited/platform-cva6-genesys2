// Copyright 2024 Capabilities Limited

#include <stdint.h>
#include "uart.h"
#include "gpio.h"

#define S_IN_NS 1000000000

int main(void)
  {
     // Setup UART
     UART_init(&g_uart_0,
             UART_115200_BAUD,
             UART_DATA_8_BITS | UART_NO_PARITY | UART_ONE_STOP_BIT);

     // Receive user input
     uint8_t prompt[20] = "Press 's' to start\n";
     char recv[1];
     while (1) {
        UART_polled_tx_string(&g_uart_0, prompt);
        while(UART_tx_complete(&g_uart_0)==0);
        int rx_n = UART_get_rx(&g_uart_0, recv, 1);
        if (rx_n > 0 && recv[0] == 's') {
          break;
        }
        nanosleep(S_IN_NS);
     }

     // Print loop
     uint8_t message[13] = "Hello World\n";
     while(1) {
        UART_polled_tx_string(&g_uart_0, message);

        while(UART_tx_complete(&g_uart_0)==0);

        // Access switches and LEDs with GPIO
        set_leds(get_switches());

        nanosleep(S_IN_NS);
     }

     return(0);
  }