# SPDX-FileCopyrightText: 2017 John Edgar Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Circuit Playground NeoPixel
import time
import board
from rainbowio import colorwheel
import neopixel
import touchio
import digitalio

pixels_board = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)
pixels_strip = neopixel.NeoPixel(board.A3, 30, brightness=0.1, auto_write=False)

buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.switch_to_input(pull=digitalio.Pull.DOWN)
buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.switch_to_input(pull=digitalio.Pull.DOWN)

builtinled = digitalio.DigitalInOut(board.D13)
builtinled.switch_to_output()

switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

btn = digitalio.DigitalInOut(board.A5)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

def color_chase(pixels, color, wait):
    for i in range(len(pixels)):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(pixels, wait):
    for j in range(255):
        for i in range(len(pixels)):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(100)


def rainbow(pixels, wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        pixels.show()
        time.sleep(wait)


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

NIGHTLIGHT_ON = 1
NIGHTLIGHT_BRIGHT = 2
NIGHTLIGHT_OFF = 3

NIGHTLIGHT_TIMEOUT = 900

state = NIGHTLIGHT_ON
print("Initiating Nightlight Loop")
first_button_press = True
j = 0
button_press_time = 0

while True:
    if buttonA.value or buttonB.value or not btn.value:  # button is pushed
        if (first_button_press):
            print("Button pressed")
            button_press_time = time.time()
            builtinled.value = True
            state = state + 1
            if state > 3:
                state = 1
        # Subsequent loops are not initial press
        first_button_press = False
    else:
        # Since button is not currently pressed, next press will be first
        builtinled.value = False
        first_button_press = True

    if state == NIGHTLIGHT_ON:
        for i in range(len(pixels_board)):
            rc_index = (i * 256 // 10) + j * 5
            pixels_board[i] = colorwheel(rc_index & 255)
        for k in range(len(pixels_strip)):
            rc_index = (k * 256 // 10) + j * 5
            pixels_strip[k] = colorwheel(rc_index & 255)
        pixels_board.show()
        pixels_strip.show()
        j = j + 1
        if (j > 255):
            j = 0
        time.sleep(0.01)
    elif state == NIGHTLIGHT_BRIGHT:
        pixels_board.fill(0xffffffff)
        pixels_board.show()
        pixels_strip.fill(0xffffffff)
        pixels_strip.show()
    else:
        pixels_board.fill(OFF)
        pixels_board.show()
        pixels_strip.fill(OFF)
        pixels_strip.show()

    if (time.time() - button_press_time > NIGHTLIGHT_TIMEOUT):
        state = NIGHTLIGHT_OFF
        time.sleep(1)
    time.sleep(0.001)
