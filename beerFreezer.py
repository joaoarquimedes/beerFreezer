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
time_freezer_last_keep_off = "tmp/time_freezer_last_keep_off.txt"
time_freezer_last_keep_on = "tmp/time_freezer_last_keep_on.txt"
json_report = "web/report/beerFreezer.json"

calc_ther_max = ther_set + ther_var_up
calc_ther_min = ther_set - ther_var_down
time_hour = '{:%H:%M}'.format(datetime.datetime.now())
time_now = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
time_next = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now() + datetime.timedelta(minutes = freezer_time_minimal_on))

if not os.path.exists(time_to_on): open(time_to_on, 'w+')
if not os.path.exists(time_freezer_last_keep_off):
    file = open(time_freezer_last_keep_off, 'w+')
    file.write(str(time_now))
    file.close()
if not os.path.exists(time_freezer_last_keep_on):
    file = open(time_freezer_last_keep_on, 'w+')
    file.write(str(time_now))
    file.close()

# Escreve log
# ------------------------------------------------
def writeLog(getLog):
    file = open(log, 'a')
    file.write(time_now+" - "+str(getLog)+"\n")
    file.close()

# Tempo limite para ligar o freezer
# ------------------------------------------------
def setTimeNext(getTimeNext):
    file = open(time_to_on, 'w')
    file.write(str(getTimeNext))
    file.close()

def getTimeNext():
    file = open(time_to_on, 'r').read()
    return file

# Tempo que o freezer manteve desligado
# ------------------------------------------------
def setFreezerLastKeepOFF(time):
    file = open(time_freezer_last_keep_off, 'w')
    file.write(str(time))
    file.close()

def getFreezerLastKeepOFF():
    file = open(time_freezer_last_keep_off, 'r').read()
    return file

# Tempo que o freezer manteve ligado
# ------------------------------------------------
def setFreezerLastKeepON(time):
    file = open(time_freezer_last_keep_on, 'w')
    file.write(str(time))
    file.close()

def getFreezerLastKeepON():
    file = open(time_freezer_last_keep_on, 'r').read()
    return file

# Escreve arquivo JSON
# ------------------------------------------------
def setJsonReport(data):
    file = open(json_report, 'a')
    file.write(str(data)+"\n")
    file.close


# Calcula o tempo em que o freezer está ligado/desligado
# ------------------------------------------------
def calcFreezerKeepState(time1, time2):
    from datetime import datetime
    fmt = '%Y-%m-%d %H:%M:%S'
    t1 = datetime.strptime(time1, fmt)
    t2 = datetime.strptime(time2, fmt)
    return str(t1 - t2)


if thermometerNOW() > calc_ther_max and freezerNOW() == 0 and time_now > getTimeNext():
    message = "Temperatura em " + str(thermometerNOW()) + "°C. Ligando o freezer"
    writeLog(message)
    freezerON()
    setFreezerLastKeepON(time_now)

if thermometerNOW() < calc_ther_min and freezerNOW() == 1:
    message = "Temperatura em " + str(thermometerNOW()) + "°C. Desligando o freezer. Freezer poderá ser ligado após " + str(time_next)
    writeLog(message)
    setTimeNext(str(time_next))
    freezerOFF()
    setFreezerLastKeepOFF(time_now)

if freezerNOW() == 0:
    freezerState = "Desligado"
    calcFreezerLastState = calcFreezerKeepState(time_now, getFreezerLastKeepOFF())
else:
    freezerState = "Ligado"
    calcFreezerLastState = calcFreezerKeepState(time_now, getFreezerLastKeepON())

json_data = {
    "data" : time_hour,
    "temperatura termometro" : thermometerNOW(),
    "temperatura setado" : ther_set,
    "limite temperatura alta" : calc_ther_max,
    "limite temperatura baixa" : calc_ther_min,
    "status do freezer" : freezerNOW(),
    "tempo freezer status" : calcFreezerLastState
}

print (" ----------------------- BeerFreezer ----------------------")
print(" -> Temperatura setado.........................", str(ther_set) + "°C")
print(" -> Variacao da temperatura para mais..........", str(ther_var_up) + "°C")
print(" -> Variacao da temperatura para menos.........", str(ther_var_down) + "°C")
print(" -> Calculo da temperatura para mais...........", str(calc_ther_max) + "°C")
print(" -> Calculo da temperatura para menos..........", str(calc_ther_min) + "°C")
print(" -> Temperatura do sensor......................", str(thermometerNOW()) + "°C")
print(" -> Tempo limite para ligar o freezer..........", str(freezer_time_minimal_on) + " minutos")
print(" -> Data atual.................................", time_now)
print(" -> Data limite para ligar o freezer...........", getTimeNext())
print(" -> Status do freezer atual....................", freezerState)
print(" -> Tempo do status (on/off)...................", calcFreezerLastState)
print (" -----------------------------------------------------------")

setJsonReport(json_data)
