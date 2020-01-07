#!/usr/bin/env python
# -*- coding: utf-8 -*-



#######################################################################
##########################|bibliotecas|################################
#######################################################################
import time

import random

from random import randint

import datetime

import serial

from ftplib import FTP

import mysql.connector as mariadb

import os

from ssd1306.oled.device import ssd1306, sh1106

from ssd1306.oled.render import canvas

from PIL import ImageFont, ImageDraw

import OPi.GPIO as GPIO

#######################################################################
######################|configuração de portas|#########################
#######################################################################

GPIO.setboard(GPIO.ZERO)

GPIO.setmode(GPIO.BOARD)


print('configurando GPIO')

botao_relatorio = 24 
botao_backup = 23
botao_cortesia = 21
botao_pago = 19

GPIO.setup(botao_relatorio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(botao_backup, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(botao_cortesia, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(botao_pago, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


print('Pressione algo')

device = ssd1306(port=0, address=0x3C)

lora = serial.Serial(
               port='/dev/ttyS2',             
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
           )

impressora = serial.Serial(
               port='/dev/ttyS1',             
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
          )

inicio_turno_1 = "00:01"  
 
fim_turno_1 = "00:00"  

#######################################################################
################|configuração de informação no display|################
#######################################################################

def screen_evo(estado, tipo, texto, valor):

    #Descanço
    if(estado == 0 and tipo == 0):
        with canvas(device) as draw:
            font1 = ImageFont.truetype('./Orange/fonts/VCR_OSD_MONO_1.001.ttf',45)
            font2 = ImageFont.truetype('./Orange/fonts/VCR_OSD_MONO_1.001.ttf',10)
            draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
            draw.text((20, 0), "EVO", font=font1, fill=255)
            draw.text((8, 45), "EVOLUCAO NO BANHO", font=font2, fill=255)
    
    #AGUARDE, ENTRANDO E GERANDO
    elif(estado== 1 and tipo == 0):
        with canvas(device) as draw:
            font1 = ImageFont.truetype('./Orange/fonts/VCR_OSD_MONO_1.001.ttf',18)
            draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
            draw.text((0, 30), texto, font=font1, fill=255)
    
    #Menu
    elif(estado== 1 and tipo == 1):
        with canvas(device) as draw:
            font1 = ImageFont.truetype('./Orange/fonts/VCR_OSD_MONO_1.001.ttf',14)
            font2 = ImageFont.truetype('./Orange/fonts/VCR_OSD_MONO_1.001.ttf',20)
            draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
            draw.text((10, 5), texto, font=font1, fill=255)
            draw.text((20, 30), valor, font=font2, fill=255)
    
    #Senha gerada
    elif(estado== 1 and tipo == 2):
        with canvas(device) as draw:
            font1 = ImageFont.truetype('./Orange/fonts/VCR_OSD_MONO_1.001.ttf',12)
            font2 = ImageFont.truetype('./Orange/fonts/VCR_OSD_MONO_1.001.ttf',30)
            draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
            draw.text((10, 5), texto, font=font1, fill=255)
            draw.text((30, 30), valor, font=font2, fill=255)

####################################################################
##########################|ENVIA LORA|##############################
####################################################################
def envia_lora(config, dado_enviar):

   dado_enviar = str(dado_enviar)
   lora.write(str(config).encode())
   time.sleep(0.2)
   lora.write((str(dado_enviar[0])).encode())
   time.sleep(0.2)
   lora.write((str(dado_enviar[1])).encode())
   time.sleep(0.2)
   lora.write((str(dado_enviar[2])).encode())
   time.sleep(0.2)
   lora.write((str(dado_enviar[3])).encode())
   time.sleep(1)
   return

#######################################################################
#####################|FUNÇÕES DE SALVAR TXT|###########################
#######################################################################

def salva_offline_pago():

        arq = open('/root/Desktop/DATABASES/DATABASE_OFFLINE_PAY.txt', 'r')
        conteudo_s = str( int(arq.read()) + 1)
        
        arq = open('/root/Desktop/DATABASES/DATABASE_OFFLINE_PAY.txt', 'w')
        arq.write(conteudo_s)
        
        arq.close()

        arq = open('/root/Desktop/DATABASES/PAY_ONLINE.txt', 'r')
        conteudo_s = str( int(arq.read()) + 1)
        
        arq = open('/root/Desktop/DATABASES/PAY_ONLINE.txt', 'w')
        arq.write(conteudo_s)
        
        arq.close()

        return

def salva_offline_cortesia():

        arq = open('/root/Desktop/DATABASES/DATABASE_OFFLINE_FREE.txt', 'r')
        conteudo_s = str( int(arq.read()) + 1)
        
        arq = open('/root/Desktop/DATABASES/DATABASE_OFFLINE_FREE.txt', 'w')
        arq.write(conteudo_s)
        
        arq.close()

        arq = open('/root/Desktop/DATABASES/FREE_ONLINE.txt', 'r')
        conteudo_s = str( int(arq.read()) + 1)
        
        arq = open('/root/Desktop/DATABASES/FREE_ONLINE.txt', 'w')
        arq.write(conteudo_s)
        
        arq.close()


        return

#######################################################################
#######################|FUNÇÃO DE RELATÓRIO|###########################
#######################################################################

def funcao_relatorio():

        screen_evo(1, 0, "AGUARDE...", 0) #AGUARDE

        #conecta_sql()

        date_now = datetime.datetime.now()
        data_ontem = date_now - datetime.timedelta(days=1)
        string_data_ontem = data_ontem.strftime('%Y-%m-%d')

        arq = open('/root/Desktop/DATABASES/DATABASE_OFFLINE_PAY.txt', 'r')
        pay_total = arq.read()
        arq.close()
        
        arq = open('/root/Desktop/DATABASES/DATABASE_OFFLINE_FREE.txt', 'r')
        free_total = arq.read()
        arq.close()

        impressora.write(" \nImpresso em: ".encode())
        impressora.write(date_now.strftime('%Y-%m-%d').encode())
        
        impressora.write('\nTOTAL GERAL PAGO: '.encode())
        impressora.write(pay_total.encode())
        
        impressora.write('\nTOTAL GERAL CORT.: '.encode())
        impressora.write(free_total.encode())

        arq = open('/root/Desktop/DATABASES/DATABASE_INCREMENTAL.txt', 'r')
        conteudo = arq.readlines()
        numlinhas = len(conteudo)
        
        for j in range(numlinhas):
        
            resposta = conteudo[j].find(string_data_ontem)

            if resposta == 0:
            
                        dados_impr = conteudo[j].split(',')
                        
                        impressora.write("\n\nData: ".encode())
                        impressora.write(string_dataBR_ontem.encode())

                        impressora.write("\nTOTAL PAGOS: ".encode())
                        impressora.write(dados_impr[1].encode())
                        
                        impressora.write("\nTOTAL CORTESIAS: ".encode())
                        impressora.write(dados_impr[2].encode())
                        impressora.write("\n".encode())
        
        time.sleep(3)
        return

#######################################################################
#####################|FUNÇÃO DE GERAR SENHA|###########################
#######################################################################
def funcao_gerar_senha():

        global senha_criada
        senha_criada = random.randrange(1000, 9999, 1)

        data_atual = datetime.datetime.now()
        data_atual_texto = data_atual.strftime('%d/%m/%Y %H:%M')

        envia_lora(1,senha_criada)

        screen_evo(1 ,2 , data_atual_texto, str(senha_criada))

        #print(data_atual_texto, senha_criada)
        impressora.write("     E V O\n".encode())
        time.sleep(0.3)
        impressora.write(" EVOLUCAO NA AUTOMACAO DO BANHO".encode())
        time.sleep(0.3)
        impressora.write("\n        ".encode())
        time.sleep(0.3)
        impressora.write(data_atual_texto.encode())
        time.sleep(0.3)
        return

def funcao_cortesia():

        global senha_criada

        impressora.write("\n   Senha Banho Cortesia:".encode())
        time.sleep(0.3)
        impressora.write(" \n\n     ".encode())
        time.sleep(0.3)
        impressora.write(str(senha_criada).encode())
        time.sleep(0.3)
        impressora.write("\n".encode())
        time.sleep(0.3)
        impressora.write("...............................".encode())
        time.sleep(0.3)
        impressora.write("\n\n\n".encode())
        time.sleep(1)

        #envia para o ZB a senha
        envia_lora(1,senha_criada)
        time.sleep(1.3)

        impressora.write("           Via do Caixa\n".encode())
        time.sleep(0.3)
        impressora.write("      E V O\n".encode())
        time.sleep(0.3)
        impressora.write(" EVOLUCAO NA AUTOMACAO DO BANHO".encode())
        time.sleep(0.3)
        impressora.write("\n        ".encode())
        time.sleep(0.3)
        impressora.write("\n   Senha Cortesia: ".encode())
        time.sleep(0.3)
        senha_criada_s = str(senha_criada)
        impressora.write(senha_criada_s.encode())
        time.sleep(0.3)
        impressora.write("\n\n No. Cupom:\n".encode())
        time.sleep(0.3)
        impressora.write("..............................".encode())
        impressora.write("\n\n\n".encode())
        time.sleep(3)

        salva_offline_cortesia()

        time.sleep(1)
        return

def funcao_pago():
        impressora.write("\n   Senha Banho Pago:".encode())
        time.sleep(0.3)
        impressora.write(" \n\n     ".encode())
        time.sleep(0.3)
        
        global senha_criada
        impressora.write(str(senha_criada).encode())
        
        impressora.write(" ".encode())
        time.sleep(0.3)
        impressora.write("\n".encode())
        time.sleep(0.3)
        impressora.write("...............................".encode())
        time.sleep(0.3)
        impressora.write("\n\n\n".encode())
        time.sleep(2)

   #envia para o ZB a senha
        envia_lora(1,senha_criada)
        time.sleep(3)

        salva_offline_pago()
        time.sleep(0.5)

        return

def funcao_menu():
        time.sleep(1)    
        passou = 0
        while(GPIO.input(botao_cortesia) == False):
                if(passou == 0):
                        arq = open('/root/Desktop/DATABASES/SENHA_MANUAL.txt', 'r')
                        senha_manual = int(arq.read())
                        arq.close()
                        screen_evo(1, 1, "Senha Manual", str(senha_manual))
                        passou = 1

        
                if (GPIO.input(botao_pago)):
                        screen_evo(1, 0, "Gerando...", 0)

                        senha_manual = random.randrange(1000, 9999, 1)
                        arq = open('/root/Desktop/DATABASES/SENHA_MANUAL.txt', 'w')
                        arq.write(str(senha_manual))
                        arq.close()
                        envia_lora(4, senha_manual)
                        
                        impressora.write("\n   Nova Senha Manual:".encode())
                        time.sleep(0.3)
                        impressora.write(" \n\n     ".encode())
                        time.sleep(0.3)
                        impressora.write(str(senha_manual).encode())
                        time.sleep(0.3)
                        impressora.write("\n".encode())
                        time.sleep(0.3)
                        impressora.write("...............................".encode())
                        time.sleep(0.3)
                        impressora.write("\n\n\n".encode())
                        time.sleep(1)
                        
                        passou = 0

        time.sleep(1)
        passou = 0

        while(GPIO.input(botao_cortesia) == False):
                if(passou == 0):
                        arq = open('/root/Desktop/DATABASES/DURACAO_BANHO.txt', 'r')
                        minutes = int(arq.read())
                        screen_evo(1, 1, 'Duracao banho', (str(minutes)+ ' min'))
                        
                        passou = 1

                if (GPIO.input(botao_pago)):
                        time.sleep(0.3)
                        while(GPIO.input(botao_pago) == False):
                                if (GPIO.input(botao_relatorio)):
                                        minutes = minutes - 1
                                        if(minutes <= 0):
                                            minutes = 1
                                
                                if (GPIO.input(botao_backup)):
                                        minutes = minutes + 1
                                        if(minutes >= 16): 
                                            minutes = 15

                                screen_evo(1, 0, (str(minutes)+ ' min'), 0)
                        
                        if(minutes >= 10):
                                envia_lora(3, (str(minutes) + '00'))
                        
                        elif(minutes < 10):
                                envia_lora(3, ('0' + str(minutes) + '00'))
                        
                        arq = open('/root/Desktop/DATABASES/DURACAO_BANHO.txt', 'w')
                        arq.write(str(minutes))
                        passou = 0

        screen_evo(0, 0, 0, 0)
        return

while True:

    screen_evo(0, 0, 0, 0)

    if (GPIO.input(botao_relatorio)):
        time.sleep(0.2)
        if (GPIO.input(botao_relatorio)):
            funcao_relatorio()
            print('relatorio')      
            time.sleep(5)

    if (GPIO.input(botao_backup)):
        time.sleep(0.2)
        if (GPIO.input(botao_backup)):
            global senha_criada
            try:
                screen_evo(1, 1, "SENHA:", str(senha_criada))
            except:
                pass

            print('ultima')
            time.sleep(5)
    
    if ((GPIO.input(botao_backup)) and GPIO.input(botao_relatorio)):
        time.sleep(0.2)
        if ((GPIO.input(botao_backup)) and GPIO.input(botao_relatorio)):
            screen_evo(1, 0, "ENTRANDO", 0)
            funcao_menu()
            time.sleep(0.5)
    
    if (GPIO.input(botao_cortesia)):
        time.sleep(0.2)
        funcao_gerar_senha()
        funcao_cortesia()
        print('cortesia')
        time.sleep(5)

    if (GPIO.input(botao_pago)):
        time.sleep(0.2)
        funcao_gerar_senha()
        funcao_pago()
        print('pago')
        time.sleep(5)
        
