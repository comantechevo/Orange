#config opara armbian Bionic

import os
import time

print('INICIANDO A CONFIGURAÇÃO DO SISTEMA')

time.sleep(2)

print('Atualizando....')
os.system("sudo apt-get update")
os.system("sudo apt-get upgrade")
os.system('clear')
print('atualizado')

time.sleep(1)

os.system('clear')
print('instalando dependencias')
os.system('sudo apt-get install python3-dev python3-pip')
os.system('sudo apt install ftp')
os.system('sudo apt-get install mariadb-server-10.3')
os.system('sudo apt install python3-pip')
os.system('sudo pip3 install mysql-connector-python')
os.system('sudo git clone https://github.com/codelectron/ssd1306/')
os.system('sudo python https://github.com/codelectron/ssd1306/setup.py install')
os.system('sudo apt install python3-pil')
os.system('sudo pip3 install pyserial')
os.system('sudo pip3 install wheel')
os.system('sudo apt-get install python3-setuptools')
os.system('sudo pip3 install OrangePi.GPIO')
os.system('sudo pip3 install smbus2')

time.sleep(1)
os.system('clear')
print('dependencias instaladas')

time.sleep(1)
os.system('clear')
print('configurando ambiente')
os.system('sudo mkdir Desktop')
os.system('sudo mkdir Desktop/DATABASES')
os.system('cp -r /root/ssd1306/ /root/Desktop/')
arq = open('Desktop/DATABASES/DATABASE_INCREMENTAL.txt', 'w')
arq.close()
arq = open('Desktop/DATABASES/DATABASE_OFFLINE_PAY.txt', 'w')
arq.write('0')
arq.close()
arq = open('Desktop/DATABASES/DATABASE_OFFLINE_FREE.txt', 'w')
arq.write('0')
arq.close()
arq = open('Desktop/DATABASES/PAY_ONLINE.txt', 'w')
arq.write('0')
arq.close()
arq = open('Desktop/DATABASES/FREE_ONLINE.txt', 'w')
arq.write('0')
arq.close()

os.system('clear')
print('atualizando Github')
os.system('git config --global credential.helper cache')
os.system('git config --global user.name "comantechevo"')
os.system('git config --global user.name "engenharia@comantech.com"')
os.system('git clone https://github.com/comantechevo/Orange.git')
os.system('cp -r /root/Orange/EVO_CENTRAL_ORANGE_PI.py /root/Desktop/')

os.system('clear')
print('apagando recorrencias')

os.system('rm -r /root/config.py')
os.system('rm -r /root/ssd1306')

print('FINALIZADO')

os.system('clear')

print('ARRUMANDO IDENTAÇÃO')

os.system('cd Orange/ && git pull origin master')
os.system('rm /root/Desktop/EVO_CENTRAL_ORANGE_PI.py')
os.system('cp -r /root/Desktop/Orange/EVO_CENTRAL_ORANGE_PI.py /root/Desktop')
os.system('cp -r /root/Desktop/Orange/corrige.py /root/Desktop')
os.system('cp -r /root/Desktop/Orange/atualiza.py /root/Desktop')
print('atualizado')
os.system('python3 corrige.py')
print('corrigido!')
