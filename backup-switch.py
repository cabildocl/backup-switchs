import sys
from netmiko import ConnectHandler
import pandas as pd
import datetime
import zipfile
import glob
import configparser
from telegramsend import *

#load variables
config = configparser.ConfigParser()
config.read('config.ini')
#variables
token_id = config["CONFIG"]["TOKEN_ID"]
group_id = config["CONFIG"]["GROUP_ID"]



listado = sys.argv[1]

df = pd.read_csv(listado)

fecha = str(datetime.datetime.today().strftime('%Y-%m-%d'))

for index, row in df.iterrows():
    try:
        ip = row["ip"]
        usuario = row["usuario"]
        clave = row["clave"]
        print (ip + " " + usuario + " " + clave)
        cisco_01 = { 'device_type':row['tipo'], 'ip':ip, 'username':usuario, 'password':clave}
        net_connect = ConnectHandler(**cisco_01)
        output = net_connect.send_command("show runn")
        nombre = str(ip)+ "-" + fecha +".txt"
        fout = open(nombre, 'w')
        fout.writelines(output)
        fout.close()
        net_connect.disconnect()
    except:
        print ("Error IP: " + ip)
        telegramsend(token_id,group_id,"\U000026A0 *Error de Respaldo* \U000026A0 " + " \nEquipo: " + ip)
telegramsend(token_id,group_id,"\U0001F37B *Termino de respaldo* \U0001F37B")

### Archivo comprimido con configuraciones
comprimido = "backup" + "-" + fecha +".zip"
zf = zipfile.ZipFile(comprimido, mode='w')
expresion =  "*" + "-" + fecha +".txt"
archivos = glob.glob(expresion)
for archivo in archivos:
 zf.write(archivo)
zf.close()

#envio del archivo
telegramsendfile(token_id,group_id,comprimido)
