# backup-switch
script for backup. You need to have a csv file with ip, type, user, password and directory of backup to your devices.

pip install -r requirements.txt
python3 backup_device.py listado.csv

Now it is support send for telegram, edit config.ini and:

python3 backup_telegram.py listado.csv config.ini


Is support:
- cisco_ios 
- cisco_s300
- cisco_wlc
- huawei
- smartzone
- vyos
- fortinet
- Mikrotik


