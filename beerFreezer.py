#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import datetime

# ###################################################
#
# CONFIGURAÇÕES
#
# ###################################################

# Qual a temperatura que deseja manter (em Celsius)?
# Exemplo: 12.0 (doze graus celsius)
TEMP_SET = 20.0

# Qual o limite de diferença tolerável para a temperatura (para mais)?
# Exemplo: 1.0 (diferença de um grau podendo variar para mais)
TEMP_VAR_UP = 1.0

# E qual o limite da temperatura para menos?
TEMP_VAR_DOWN = 1.5

# Qual o tempo (em minutos) mínimo para poder ligar o freezer depois de uma parada?
# Este tempo irá respeitar o limite mínimo antes de ligar o equipamento calculando o valor
# da última vez em que o mesmo foi desligado.
# OBS.: Tempo abaixo de 6 minutos pode ser danificar o aparelho. Consulte o manual do seu freezer.
FREEZER_TIME_LIMITE_ON = 8




# --------- PROGRAMAÇÃO --------- #

# TERMOSTATO
# #################################
import therm
from therm import thermometerNOW

# RELAY
# ################################
import relay
from relay import freezerON
from relay import freezerOFF
from relay import freezerNOW

temp_up = TEMP_SET + TEMP_VAR_UP
temp_down = TEMP_SET - TEMP_VAR_DOWN
time_now = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
time_next = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now() + datetime.timedelta(minutes = FREEZER_TIME_LIMITE_ON))

while True:
    if thermometerNOW() > temp_up and freezerNOW() == 0 : freezerON()
    if thermometerNOW() < temp_down and freezerNOW() == 1 : freezerOFF()
    
    if freezerNOW() == 0 : freezerState = "Desligado"
    if freezerNOW() == 1 : freezerState = "Ligado"
    
    print (" ------------------ BeerFreezer ------------------")
    print(" -> Temperatura setado.........................", TEMP_SET, "°C")
    print(" -> Variacao da temperatura para mais..........", TEMP_VAR_UP, "°C")
    print(" -> Variacao da temperatura para menos.........", TEMP_VAR_DOWN, "°C")
    print(" -> Calculo da temperatura para mais...........", temp_up, "°C")
    print(" -> Calculo da temperatura para menos..........", temp_down, "°C")
    print(" -> Temperatura do sensor......................", thermometerNOW(), "°C")
    print(" -> Tempo limite para ligar o freezer..........", FREEZER_TIME_LIMITE_ON, "minutos")
    print(" -> Data atual.................................", time_now)
    print(" -> Data limite para ligar o freezer...........", time_next)
    print(" -> Status do freezer atual....................", freezerState)
    
    time.sleep(3)




