def cisco_ios(IP, USER, PASSWORD):
    from netmiko import ConnectHandler
    import datetime
    DATE = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    device = { 'device_type':'cisco_ios', 'ip':IP, 'username':USER, 'password':PASSWORD}
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show runn")
    name_file = "/tmp/" + str(IP)+ "-" + DATE +".txt"
    file_config = open(name_file, 'w')
    file_config.writelines(output)
    file_config.close()
    net_connect.disconnect()
    return name_file
def cisco_s300(IP, USER, PASSWORD):
    from netmiko import ConnectHandler
    import datetime
    DATE = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    device = { 'device_type':'cisco_s300', 'ip':IP, 'username':USER, 'password':PASSWORD}
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show runn")
    name_file = "/tmp/" + str(IP)+ "-" + DATE +".txt"
    file_config = open(name_file, 'w')
    file_config.writelines(output)
    file_config.close()
    net_connect.disconnect()
    return name_file
def huawei(IP, USER, PASSWORD):
    from netmiko import ConnectHandler
    import datetime
    DATE = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    device = { 'device_type':'huawei', 'ip':IP, 'username':USER, 'password':PASSWORD,'global_delay_factor': 5}
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("display current")
    name_file = "/tmp/" + str(IP)+ "-" + DATE +".txt"
    file_config = open(name_file, 'w')
    file_config.writelines(output)
    file_config.close()
    net_connect.disconnect()
    return name_file
def smartzone(IP,USER,PASSWORD):
    import requests
    import time
    import datetime
    import json
    URL = "https://" + IP + ":7443"
    DATE = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    headers = {'content-type': 'application/json'}
    payload = {'username' : USER, 'password' : PASSWORD}
    connection1 = URL + "/api/public/v6_0/session" 
    response1 = requests.post( connection1, data=json.dumps(payload),headers=headers ,verify=False )
    cookie =response1.headers["Set-Cookie"]
    headers = {'content-type': 'application/json', 'Cookie': cookie}
    connection2 = URL + "/api/public/v6_0/configuration/backup"
    response2 = requests.post( connection2, data=json.dumps(payload),headers=headers ,verify=False )
    backup_id=eval(response2.text)
    time.sleep(180)
    connection3 = URL + "/api/public/v6_0/configuration/download"
    params = {"backupUUID": backup_id['id']}
    response3 = requests.get( connection3, data=json.dumps(payload), params=params,headers=headers ,verify=False )
    name_file = "/tmp/" + str(IP)+ "-" + DATE +".txt"
    file_config = open(name_file, 'wb')
    file_config.writelines(response3.content)
    file_config.close()
    connection4 = URL + "/api/public/v6_0/configuration/" + backup_id['id']
    response4 = requests.delete( connection4, data=json.dumps(payload),headers=headers ,verify=False )
    return name_file





