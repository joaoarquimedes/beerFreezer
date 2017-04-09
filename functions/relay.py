#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO

# Define o número da pinagem do respbarry de controle do relay
pNumber = 11

def boardStart():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

def setGPIOOut(pNumber):
    GPIO.setup(pNumber, GPIO.OUT)

def freezerON():
    if GPIO.input(pNumber) == 0:
        GPIO.output(pNumber, 1)

def freezerOFF():
    if GPIO.input(pNumber) == 1:
        GPIO.output(pNumber, 0)

def freezerNOW():
    return GPIO.input(pNumber)

boardStart()
setGPIOOut(pNumber)