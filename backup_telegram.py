def telegram_backups(BATCH_FILE):
    from telegramsend import telegramsend, telegramsendfile
    from backup_device import backup
    import pandas as pd
    import datetime
    import zipfile
    import glob
    import configparser
    import os
    #load variables
    config = configparser.ConfigParser()
    config.read('config.ini')
    #variables
    token_id = config["CONFIG"]["TOKEN_ID"]
    group_id = config["CONFIG"]["GROUP_ID"]
    date_today = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    name_file=os.path.splitext(os.path.basename(BATCH_FILE))[0]
    """
    CSV FILE
    ip,user,password,type,directory
    """
    df = pd.read_csv(BATCH_FILE)
    config_zip = f"/tmp/{name_file}-{date_today}.zip"
    zf = zipfile.ZipFile(config_zip, mode='w')
    print(config_zip)
    for index, row in df.iterrows():
        try:
            backup_file=backup(row['ip'],row['user'],row['password'],row['type'],row['directory'])
            print(backup_file)
            zf.write(backup_file)
        except:
            print (f"Error IP: {row['ip']}")
            telegramsend(token_id,group_id,f"\U000026A0 *Backup Error* \U000026A0 \nSite: {name_file} \nDevice: {row['ip']}")
    zf.close()
    telegramsend(token_id,group_id,f"\U0001F37B *Backup Completed* \U0001F37B \nSite: {name_file}")
    telegramsendfile(token_id,group_id,config_zip)
    return 0
if __name__ == '__main__':
    import sys
    telegram_backups(sys.argv[1])
