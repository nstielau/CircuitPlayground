# SPDX-FileCopyrightText: 2017 John Edgar Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Circuit Playground NeoPixel
import time
import board
from rainbowio import colorwheel
import neopixel
import touchio
import analogio
import digitalio
import simpleio


import adafruit_thermistor

touch_A4 = touchio.TouchIn(board.A4)
touch_A5 = touchio.TouchIn(board.A5)
touch_A6 = touchio.TouchIn(board.A6)
touch_TX = touchio.TouchIn(board.TX)

pixels_board = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)
pixels_strip = neopixel.NeoPixel(board.A3, 30, brightness=0.1, auto_write=False)
thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)
light = analogio.AnalogIn(board.LIGHT)
buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.switch_to_input(pull=digitalio.Pull.DOWN)
buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.switch_to_input(pull=digitalio.Pull.DOWN)

builtinled = digitalio.DigitalInOut(board.D13)
builtinled.switch_to_output()

switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# choose which demos to play
# 1 means play, 0 means don't!
color_chase_demo = 0
flash_demo = 0
rainbow_demo = 0
rainbow_cycle_demo = 1

initial_temp = 0
initial_light = 0


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
        time.sleep(get_wait())


def rainbow(pixels, wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        pixels.show()
        time.sleep(wait)


def get_wait():
    wait = 0.05
    if touch_TX.value:
        # print("TX touched!")
        return wait / 10
    if touch_A6.value:
        # print("A6 touched!")
        return wait / 6
    if touch_A5.value:
        # print("A5 touched!")
        return wait / 3
    if touch_A4.value:
        # print("A4 touched!")
        return wait / 2

    return wait


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

while True:
    temp_c = thermistor.temperature
    temp_f = thermistor.temperature * 9 / 5 + 32
    if initial_temp == 0:
        initial_temp = temp_f
    print(
        "Temperature is: %f C and %f F, %fF above intitial"
        % (temp_c, temp_f, temp_f - initial_temp)
    )

    peak = simpleio.map_range(light.value, 2000, 62000, 0, 9)
    if initial_light == 0:
        initial_light = peak
    print(
        "Light is %f normalized to %f, %f above initial"
        % (light.value, peak, peak - initial_light)
    )

    if buttonA.value:  # button is pushed
        builtinled.value = True
        print("Button A pressed")
    elif buttonB.value:
        builtinled.value = True
        print("Button B pressed")
    else:
        builtinled.value = False

    print("Slide is %s" % (switch.value and "Left" or "Right"))

    if color_chase_demo:
        color_chase(
            pixels_board, RED, 0.1
        )  # Increase the number to slow down the color chase
        color_chase(pixels_board, YELLOW, 0.1)
        color_chase(pixels_board, GREEN, 0.1)
        color_chase(pixels_board, CYAN, 0.1)
        color_chase(pixels_board, BLUE, 0.1)
        color_chase(pixels_board, PURPLE, 0.1)
        color_chase(pixels_board, OFF, 0.1)

    if flash_demo:
        pixels_board.fill(RED)
        pixels_board.show()
        # Increase or decrease to change the speed of the solid color change.
        time.sleep(1)
        pixels_board.fill(GREEN)
        pixels_board.show()
        time.sleep(1)
        pixels_board.fill(BLUE)
        pixels_board.show()
        time.sleep(1)
        pixels_board.fill(WHITE)
        pixels_board.show()
        time.sleep(1)

    if rainbow_cycle_demo:
        # rainbow_cycle(
        # pixels_board, get_wait()
        # )  # Increase the number to slow down the rainbow.
        rainbow_cycle(
            pixels_strip, get_wait()
        )  # Increase the number to slow down the rainbow.

    if rainbow_demo:
        #      rainbow(
        #          pixels_board, get_wait()
        #      )  # Increase the number to slow down the rainbow.
        rainbow(
            pixels_strip, get_wait()
        )  # Increase the number to slow down the rainbow.
