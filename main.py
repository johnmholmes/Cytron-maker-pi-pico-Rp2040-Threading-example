#This code is for demonstrating how you could create a traffic light with a push button
#to start a delay for a pedestrian to cross safely. It will use both cores of the Pi Pico and this is achived
#by using the built in Micropython library _thread. This use 1 core to monitor the button press while the other core
#runs the light sequence.

#The original sketch comes from the Raspberry Pi get started with micropython on the Raspberry Pi Pico ebook.
#To work on the Cryton maker pi board I use I need to change some of the code hence the video


# Gives us access to the Picos GP pins
import machine
# Gives access to use delays within the code
import utime
# Gives access to the use of both cores on the Pico be aware we can only have 1 thread running on ech core on the Pi Pico 2040
import _thread

## We declare 5 variables for the GP pins used 
led_red = machine.Pin(28, machine.Pin.OUT)
led_amber = machine.Pin(27, machine.Pin.OUT)
led_green = machine.Pin(26, machine.Pin.OUT)
button = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.Pin(22, machine.Pin.OUT)

#We also declare a global variable which we need to do alter the variable in the function _thread
# We also set it to False at startup
global button_pressed
button_pressed = False

# This function is use to check if the button has been press and starts the thread on core 1
def button_reader_thread():
    global button_pressed
    while True:
        if button.value() == False:
            button_pressed = True
        utime.sleep(0.01)
_thread.start_new_thread(button_reader_thread, ())

# We set the value for button pressed to be False before the while true so the if statement will not get run at first.

# Once the code has started outside of the if statement at line 58 and the button gets pressed.
# The second core will pick up that the button has been pressed and it will set the global variable button_pressed to True.
# Then once the code has complete line 69 it wil then come back up to the if statement and as it is true it will set the red led
# to red and then run the buzzer for loop

while True:
    if button_pressed == True:
        led_red.value(1)
        utime.sleep(1.5)
        for i in range(10):
            buzzer.value(1)
            utime.sleep(0.2)
            buzzer.value(0)
            utime.sleep(0.2)
        global button_pressed
        button_pressed = False
        
        
    led_red.value(1)
    utime.sleep(10)
    led_amber.value(1)
    utime.sleep(3)
    led_red.value(0)
    led_amber.value(0)
    led_green.value(1)
    utime.sleep(10)
    led_green.value(0)
    led_amber.value(1)
    utime.sleep(3)
    led_amber.value(0)