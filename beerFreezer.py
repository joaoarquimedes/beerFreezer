#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import ConfigParser



# Importando arquivo de configuração e setando a classe
# -------------------------------------------------------------------------------
config_file = "config.ini"
if not os.path.exists(config_file):
    print("Favor, renomear o arquivo config.ini.dist para config.ini")
    quit()

configParser = ConfigParser.ConfigParser()
configParser.read(config_file)

class Config():
    def setVersion(self, version):
        self.version = version
    def getVersion(self):
        return self.version

    def setThermometerSet(self, thermometerSet):
        self.thermometerSet = thermometerSet
    def getThermometerSet(self):
        return self.thermometerSet

    def setThermometerMax(self, thermometerMax):
        self.thermometerMax = thermometerMax
    def getThermometerMax(self):
        return self.thermometerMax + self.getThermometerSet()

    def setThermometerMin(self, thermometerMin):
        self.thermometerMin = thermometerMin
    def getThermometerMin(self):
        return self.getThermometerSet() - self.thermometerMin

    def setFreezerTimeMinON(self, freezerTimeMinON):
        self.freezerTimeMinON = freezerTimeMinON
    def getFreezerTimeMinON(self):
        return self.freezerTimeMinON


conf = Config()
conf.setVersion(configParser.get('VERSION', 'version'))
conf.setThermometerSet(float(configParser.get('GLOBAL', 'THER_SET')))
conf.setThermometerMax(float(configParser.get('GLOBAL', 'THER_VAR_UP')))
conf.setThermometerMin(float(configParser.get('GLOBAL', 'THER_VAR_DOWN')))
conf.setFreezerTimeMinON(int(configParser.get('GLOBAL', 'FREEZER_TIME_MINIMAL_ON')))



# Reconhecendo arquivos em outro diretório
# -------------------------------------------------------------------------------
sys.path.insert(0, 'functions/')

# TERMOSTATO
import therm
from therm import thermometerNOW

# RELAY
import relay
from relay import freezerON
from relay import freezerOFF
from relay import freezerNOW # 0=desligado, 1=ligado

# LCD
# Exemplo:
import RPi_I2C_driver
from RPi_I2C_driver import *

mylcd = RPi_I2C_driver.lcd()
# Exemplos LCD (escrrver no máximo 16 caracteres):
# Escrevendo na linha 1
# mylcd.lcd_display_string("RPi I2C test   ", 1)
# Escrevendo na linha 2
# mylcd.lcd_display_string("Custom chars   ", 2)
# Limpando a tela
# mylcd.lcd_clear()
# Apagando o display
# mylcd.backlight(0)

mylcd.lcd_clear()
mylcd.lcd_display_string("  beerFreezer   ", 1)
mylcd.lcd_display_string("  Starting...   ", 2)
sleep(1.5)



# Setando arquivos temporários e de log's
# -------------------------------------------------------------------------------
log = "log/beerFreezer.log"
json_report = "web/report/beerFreezer.json"



# Setando variáveis de tempo
# -------------------------------------------------------------------------------
class Time():
    def getTimeNow(self):
        return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    def getTimeDay(self):
        return '{:%d/%m/%Y}'.format(datetime.datetime.now())

    def getTimeHour(self):
        return '{:%H:%M:%S}'.format(datetime.datetime.now())

    def setTimeNextFreezerON(self, timeNextFreezerON):
        self.timeNextFreezerON = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now() + datetime.timedelta(minutes = timeNextFreezerON))
    def getTimeNextFreezerON(self):
        return self.timeNextFreezerON

    def getCalcFreezerKeepState(self, time):
        from datetime import datetime
        fmt = '%Y-%m-%d %H:%M:%S'
        t1 = datetime.strptime(self.getTimeNow(), fmt)
        t2 = datetime.strptime(time, fmt)
        return str(t1 - t2)

    def setTimeNextFreezerKeepONOFF(self):
        self.timeNextFreezerKeepONOFF = self.getTimeNow()
    def getTimeNextFreezerKeepONOFF(self):
        return self.getCalcFreezerKeepState(self.timeNextFreezerKeepONOFF)

    def setManyTimesFreezerON(self, n):
        self.manyTimesFreezerON = n
    def getManyTimesFreezerON(self):
        return self.manyTimesFreezerON

    def setManyTimesFreezerOFF(self, n):
        self.manyTimesFreezerOFF = n
    def getManyTimesFreezerOFF(self):
        return self.manyTimesFreezerOFF

mytime = Time()
mytime.setTimeNextFreezerON(0)
mytime.setTimeNextFreezerKeepONOFF()
mytime.setManyTimesFreezerON(0)
mytime.setManyTimesFreezerOFF(0)



# Definindo funções para escrita em arquivo
# -------------------------------------------------------------------------------
# Escreve log
def writeLog(getLog):
    file = open(log, 'a')
    file.write(mytime.getTimeNow() + " - " + str(getLog) + "\n")
    file.close()

# Escreve arquivo JSON
def setJsonReport(data):
    file = open(json_report, 'a')
    file.write(str(data) + "\n")
    file.close



# Freezer Engine
# -------------------------------------------------------------------------------
try:
    countON = 0
    countOFF = 0
    while True:
        if thermometerNOW() > conf.getThermometerMax() and freezerNOW() == 0 and mytime.getTimeNow() > mytime.getTimeNextFreezerON():
            freezerON()
            mytime.setTimeNextFreezerKeepONOFF()
            countON += 1
            mytime.setManyTimesFreezerON(countON)
            message = "Temperatura em " + str(thermometerNOW()) + "°C. Freezer ligado"
            writeLog(message)

        if thermometerNOW() < conf.getThermometerMin() and freezerNOW() == 1:
            mytime.setTimeNextFreezerON(conf.getFreezerTimeMinON())
            freezerOFF()
            countOFF += 1
            mytime.setManyTimesFreezerOFF(countOFF)
            mytime.setTimeNextFreezerKeepONOFF()
            message = "Temperatura em " + str(thermometerNOW()) + "°C. Freezer desligado. Freezer poderá ser ligado após " + str(mytime.getTimeNextFreezerON())
            writeLog(message)

        if freezerNOW() == 0:
            freezerState = "OFF"
            countONOFF = mytime.getManyTimesFreezerOFF()
        else:
            freezerState = "ON"
            countONOFF = mytime.getManyTimesFreezerON()

        json_data = {
            "data" : mytime.getTimeHour(),
            "temperatura termometro" : thermometerNOW(),
            "temperatura setado" : conf.getThermometerSet(),
            "limite temperatura alta" : conf.getThermometerMax(),
            "limite temperatura baixa" : conf.getThermometerMin(),
            "status do freezer" : freezerNOW(),
            "tempo freezer status" : mytime.getTimeNextFreezerKeepONOFF()
        }

        print (" ----------------------- BeerFreezer ----------------------")
        print(" -> Temperatura setado.........................", str(conf.getThermometerSet()))
        print(" -> Variacao da temperatura para mais..........", str(conf.getThermometerMax()))
        print(" -> Variacao da temperatura para menos.........", str(conf.getThermometerMin()))
        print(" -> Temperatura do sensor......................", str(thermometerNOW()))
        print(" -> Tempo limite para ligar o freezer..........", str(conf.getFreezerTimeMinON()))
        print(" -> Data atual.................................", str(mytime.getTimeNow()))
        print(" -> Data limite para ligar o freezer...........", str(mytime.getTimeNextFreezerON()))
        print(" -> Status do freezer atual....................", str(freezerState))
        print(" -> Tempo do status (on/off)...................", str(mytime.getTimeNextFreezerKeepONOFF()))
        print(" -> Quantas vezes ligou/desligou...............", str(countONOFF))
        print (" -----------------------------------------------------------")

        # Exportando dados para o Json
        setJsonReport(json_data)

        # Escrevendo no display        
        mylcd.lcd_clear()
        loop = 25
        for x in range(0, loop):
            mylcd.lcd_display_string("  Thermometer  ", 1)
            mylcd.lcd_display_string("     " + str(thermometerNOW()) + "\337C", 2)
            sleep(2)

        mylcd.lcd_clear()
        loop = 12
        for x in range(0, loop):
            mylcd.lcd_display_string("   " + str(mytime.getTimeDay()), 1)
            mylcd.lcd_display_string("    " + str(mytime.getTimeHour()), 2)
            sleep(1)

        mylcd.lcd_clear()
        loop = 7
        for x in xrange(0,loop):
            mylcd.lcd_display_string("Freezer: " + str(freezerState) + "  " + str(countONOFF) + "x", 1)
            mylcd.lcd_display_string(str(mytime.getTimeNextFreezerKeepONOFF()), 2)
            sleep(1)

        if thermometerNOW() > conf.getThermometerMax() and freezerNOW() == 0 and mytime.getTimeNow() < mytime.getTimeNextFreezerON():
            mylcd.lcd_display_string("Allow Freezer ON" + str(freezerState), 1)
            mylcd.lcd_display_string(str(mytime.getTimeNextFreezerON()), 2)
            sleep(5)

        mylcd.lcd_clear()
        mylcd.lcd_display_string("Reload...", 1)

except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print(" .... Stopping beeFreezer!")
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Stopping...", 1)
    sleep(2)
    mylcd.lcd_clear()
    mylcd.backlight(0)
    freezerOFF()

