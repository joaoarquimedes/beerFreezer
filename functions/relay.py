#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import sys
import time

# Define o número da pinagem do respbarry de controle do relay
pNumber = 11

def boardStart():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

def setGPIOOut(pNumber):
    GPIO.setup(pNumber, GPIO.OUT)

def freezerON():
    GPIO.output(pNumber, 1)

def freezerOFF():
    GPIO.output(pNumber, 0)

def freezerNOW():
    portState = GPIO.input(pNumber)
    return portState

boardStart()
setGPIOOut(pNumber)
