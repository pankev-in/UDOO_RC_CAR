UDOO_RC_CAR
===========
Autonomous RC Car using UDOO

Remotely control an RC Car using a Udoo Controller. The goal is to have a better understanding of how communications between multiple Computers/Microprocessors actually works. The UDOO controller is a simple ARM computer with an extra Arduino Due(Atmel SAM3X8E 3,3V) on board, which allows developer to implanted it very easily.

- Sending: a smartphone/computer application which allows the user to control the Car
- Listening: a python Server will be connected with that application using TCP/UDP and send commands to the low-level-controller(Atmel chip)
- Controlling: a programmed Atmel chip will be listening to the serial commands form the Server program and use them to control the motor/Servo movements.

__NEED | Tools/Material__
- 1x Laptop with Java
- 1x Android Phone
- 1x RC Car
- 1x H-Bridge Motor Controller / Standart RC-Car Receiver
- 1x Udoo controller(dual/quad)
- Batteries (I used 1x 7Ah 5V liPo + 1x 2.3Ah 12V Li-ion)
