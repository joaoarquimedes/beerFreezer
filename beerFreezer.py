#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime

# importando arquivo de configuração
config_file = "config.ini"
if not os.path.exists(config_file):
    print("Favor, renomear o arquivo config.ini.dist para config.ini")
    quit()

import configparser
config = configparser.ConfigParser()
config.read(config_file, encoding='utf-8')

version = config.get('VERSION', 'version')
ther_set = float(config.get('GLOBAL', 'THER_SET'))
ther_var_up = float(config.get('GLOBAL', 'THER_VAR_UP'))
ther_var_down = float(config.get('GLOBAL', 'THER_VAR_DOWN'))
freezer_time_minimal_on = int(config.get('GLOBAL', 'FREEZER_TIME_MINIMAL_ON'))


# Reconhecendo arquivos em outro diretório
sys.path.insert(0, 'functions/')

# TERMOSTATO
import therm
from therm import thermometerNOW

# RELAY
import relay
from relay import freezerON
from relay import freezerOFF
from relay import freezerNOW # 0=desligado, 1=ligado

log = "log/beerFreezer.log"
time_to_on = "tmp/time_to_on.txt"

if not os.path.exists(time_to_on): open(time_to_on, 'w+')

temp_up = ther_set + ther_var_up
temp_down = ther_set - ther_var_down
time_now = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
time_next = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now() + datetime.timedelta(minutes = freezer_time_minimal_on))

def writeLog(getLog):
    file = open(log, 'a')
    file.write(time_now+" - "+str(getLog)+"\n")
    file.close()

def setTimeNext(getTimeNext):
    file = open(time_to_on, 'w')
    file.write(str(getTimeNext))
    file.close()

def getTimeNext():
    file = open(time_to_on, 'r').read()
    return file


while True:
    if thermometerNOW() > temp_up and freezerNOW() == 0 and time_now > getTimeNext():
        message = "Temperatura em " + str(thermometerNOW()) + "°C. Ligando o freezer"
        print(message, sep='')
        writeLog(message)
        freezerON()
    
    if thermometerNOW() < temp_down and freezerNOW() == 1:
        message = "Temperatura em " + str(thermometerNOW()) + "°C. Desligando o freezer. Freezer poderá ser ligado após " + str(time_next)
        print(message, sep='')
        writeLog(message)
        setTimeNext(str(time_next))
        freezerOFF()
    
    if freezerNOW() == 0:
        freezerState = "Desligado"
    else:
        freezerState = "Ligado"
   
    print (" ------------------ BeerFreezer ------------------")
    print(" -> Temperatura setado.........................", str(ther_set) + "°C")
    print(" -> Variacao da temperatura para mais..........", str(ther_var_up) + "°C")
    print(" -> Variacao da temperatura para menos.........", str(ther_var_down) + "°C")
    print(" -> Calculo da temperatura para mais...........", str(temp_up) + "°C")
    print(" -> Calculo da temperatura para menos..........", str(temp_down) + "°C")
    print(" -> Temperatura do sensor......................", str(thermometerNOW()) + "°C")
    print(" -> Tempo limite para ligar o freezer..........", str(freezer_time_minimal_on) + " minutos")
    print(" -> Data atual.................................", time_now)
    print(" -> Data limite para ligar o freezer...........", getTimeNext())
    print(" -> Status do freezer atual....................", freezerState)
    
    time.sleep(3)




