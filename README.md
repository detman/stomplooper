# stomplooper
raspberry driven stompbox with looper

state of this project:
  * basic controlling and recording is done
  * audio output is work in progress

This is a raspberry project (Im using the raspberry 3)
Using two LEDs (red and yellow), and a push button (with hardware pullup resistor)

when clicking the button, the hit is recorded.
wenn holding the button pressed, the playback starts.
playback happens in the sae rythm as you recorded it.

The red led flashes every time you hit the push button (light on when pressed, light off when released),
the yellow button indicates the playback is running.

The programm is event driven; take a look at the "momentarybutton" class.

Because the application is controlled by hitting the button for short or long time, event detection is critical.

Notes:
 * I had some problems with the signal edge detection. 
 * I decided to wait some millisecs before reading out the status of the button - that fixed my problem.
 * See https://www.raspberrypi.org/forums/viewtopic.php?t=134394 for details.

THIS SCRIPT COMES WITH NO WARRANTY

Copyright Detlef Hüttemann (c) 2016 http://www.detlef-huettemann.com
