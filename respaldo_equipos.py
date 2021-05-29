from telegramsend import *
from backup_device import *
import pandas as pd
import sys
import datetime


listado = sys.argv[1]

df = pd.read_csv(listado)

fecha = str(datetime.datetime.today().strftime('%Y-%m-%d'))

for index, row in df.iterrows():
    try:
        ip = row["ip"]
        usuario = row["usuario"]
        clave = row["clave"]
        tipo = row["tipo"]
        print (ip + " " + usuario + " " + clave)
        if "cisco_ios" == tipo:
            respaldo=cisco_ios(ip, usuario, clave)
        elif "cisco_s300" == tipo:
            respaldo=cisco_s300(ip, usuario, clave)
        elif "huawei" == tipo:
            respaldo=huawei(ip, usuario, clave)
    except:
        print ("Error IP: " + ip)
        
