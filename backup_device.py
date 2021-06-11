def cisco_ios(IP, USER, PASSWORD, DIRECTORY="/tmp/"):
    from netmiko import ConnectHandler
    import datetime
    DATE = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    device = { 'device_type':'cisco_ios', 'ip':IP, 'username':USER, 'password':PASSWORD,'global_delay_factor': 4}
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show runn")
    name_file = DIRECTORY + str(IP)+ "-" + DATE +".txt"
    file_config = open(name_file, 'w')
    file_config.writelines(output)
    file_config.close()
    net_connect.disconnect()
    return name_file
def cisco_s300(IP, USER, PASSWORD, DIRECTORY="/tmp/"):
    from netmiko import ConnectHandler
    import datetime
    DATE = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    device = { 'device_type':'cisco_s300', 'ip':IP, 'username':USER, 'password':PASSWORD,'global_delay_factor': 4}
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show runn")
    name_file = DIRECTORY + str(IP)+ "-" + DATE +".txt"
    file_config = open(name_file, 'w')
    file_config.writelines(output)
    file_config.close()
    net_connect.disconnect()
    return name_file
def huawei(IP, USER, PASSWORD, DIRECTORY="/tmp/"):
    from netmiko import ConnectHandler
    import datetime
    DATE = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    device = { 'device_type':'huawei', 'ip':IP, 'username':USER, 'password':PASSWORD,'global_delay_factor': 5}
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("display current")
    name_file = DIRECTORY + str(IP)+ "-" + DATE +".txt"
    file_config = open(name_file, 'w')
    file_config.writelines(output)
    file_config.close()
    net_connect.disconnect()
    return name_file
def smartzone(IP,USER,PASSWORD, DIRECTORY="/tmp/"):
    import requests
    import time
    import datetime
    import json
    requests.packages.urllib3.disable_warnings()
    URL = "https://" + IP + ":7443"
    DATE = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    headers = {'content-type': 'application/json'}
    payload = {'username' : USER, 'password' : PASSWORD}
    #connection1 = URL + "/api/public/v6_0/session" 
    response1 = requests.post( f"{URL}/api/public/v6_0/session", data=json.dumps(payload),headers=headers ,verify=False )
    #response1 = requests.post( connection1, data=json.dumps(payload),headers=headers ,verify=False )
    cookie =response1.headers["Set-Cookie"]
    headers = {'content-type': 'application/json', 'Cookie': cookie}
    connection2 = URL + "/api/public/v6_0/configuration/backup"
    response2 = requests.post( connection2, data=json.dumps(payload),headers=headers ,verify=False )
    backup_id=eval(response2.text)
    time.sleep(180)
    connection3 = URL + "/api/public/v6_0/configuration/download"
    params = {"backupUUID": backup_id['id']}
    response3 = requests.get( connection3, data=json.dumps(payload), params=params,headers=headers ,verify=False )
    name_file = DIRECTORY + str(IP)+ "-" + DATE +".bak"
    print(response3.headers.get('content-type'))
    try:
        file_config = open(name_file, 'wb')
        file_config.write(response3.content)
    except:
        #print(response3.content)
        file_config = open(name_file, 'w')
        file_config.writelines(response3.content)
    file_config.close()
    connection4 = URL + "/api/public/v6_0/configuration/" + backup_id['id']
    response4 = requests.delete( connection4, data=json.dumps(payload),headers=headers ,verify=False )
    return name_file

def backup(IP,USER,PASSWORD, TYPE, DIRECTORY="/tmp/"):
    try:
        if "cisco_ios" == TYPE:
            file_backup=cisco_ios(IP,USER,PASSWORD, DIRECTORY)
        elif "cisco_s300" == TYPE:
            file_backup=cisco_s300(IP,USER,PASSWORD, DIRECTORY)
        elif "huawei" == TYPE:
            file_backup=huawei(IP,USER,PASSWORD, DIRECTORY)
        elif "huawei" == TYPE:
            file_backup=smartzone(IP,USER,PASSWORD, DIRECTORY)
        print(file_backup)
    except:
        print (f"Error TYPE: {TYPE}")
def batch_backups(BATCH_FILE):
    import pandas as pd
    """
    CSV FILE
    ip,user,password,type,directory
    """
    df = pd.read_csv(BATCH_FILE)
    for index, row in df.iterrows():
        try:
            backup(row['ip'],row['user'],row['password'],row['type'],row['directory'])
        except:
            print (f"Error IP: {row['ip']}")