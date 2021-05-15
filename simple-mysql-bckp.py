# add in path (MySQL bin folder) - ( Environment Varibles->Path->New ) 

import os
import subprocess
import requests
from datetime import datetime
from pathlib import Path

projectName     = 'mskoko'
apiURL          = 'http://localhost'

host            = 'localhost'
port            = 3306
dbuser          = 'root'
dbPass          = ''
dbName          = 'db_name'


d               = datetime.now()
print("Start backup time:", d.strftime("%H-%M - %d-%m-%Y"))

# Creating folder definition
def create_folder(folder_path):
    try:
        os.mkdir(folder_path, 0o755)
    except OSError:
        return False;
    else:
        return True;

# Backup definiton
def backup_db(db_host, db_port, db_user, db_pass, db_name, project_name):
    # Format file name by date: 22-10 - 11-12-2021
    fileformat = d.strftime("%H_%M_%d_%m_%Y")
    # Create folder
    if(create_folder(project_name+'/'+fileformat) == True):
        # File name
        filename = project_name + '_' + fileformat+'.sql'
        # Starting process for create backup file (mysqldump)
        p1 = subprocess.Popen(
            'mysqldump -h '+db_host+' -P '+db_port+' -u '+db_user+' -p"'+db_pass+'" '+db_name+' > '+filename, shell=True)
        # Return code
        if(p1.wait() == 0):
            if(Path(filename).rename(project_name+'/'+fileformat+'/'+filename)):
                r = True
            else:
                r = False
        else:
            r = False
        return r
    else:
        print('Wrong! | ' + project_name + ' is not created DB backup..')

# Send mail notification
def send_me_info(ur, status):
    x = requests.get(
        ur+'/process?Backup&Type=DB&Status='+status)
    if(x.status_code == 200):
        return True
    else:
        return False

# Execute
if(backup_db(db_host=host, db_port=port, db_user=dbUser, db_pass=dbPass, db_name=dbName, project_name=projectName) == True):
    print('BSP database has backup! *SUCCESS*')
    send_me_info(ur=apiURL, status='True')
else:
    print('BSP DB has not backup! *WRONG*')
    send_me_info(ur=apiURL, status='False')