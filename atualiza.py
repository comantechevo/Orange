import os

os.system('cd Orange/ && git pull origin master')
os.system('rm /root/Desktop/EVO_CENTRAL_ORANGE_PI.py')
os.system('cp -r /root/Desktop/Orange/EVO_CENTRAL_ORANGE_PI.py /root/Desktop')
os.system('cp -r /root/Desktop/Orange/corrige.py /root/Desktop')
os.system('cp -r /root/Desktop/Orange/atualiza.py /root/Desktop')
print('atualizado')
os.system('python3 corrige.py')
print('corrigido!')