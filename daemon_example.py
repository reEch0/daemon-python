#!/usr/bin/python3
import time
from daemon import Daemon
import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify
import subprocess
import sys
import os
import logging
import pathlib
logging.basicConfig(level=logging.INFO, filename='mes_log.log', filemode='w')

#ps -ef | grep python для просмотра рабочих процессов

path = pathlib.Path(__file__).parent.resolve()

def checkCommit(folder):
    subprocess.run(['git', f'--git-dir={path}/{folder}/.git', 'fetch'])
    commit = subprocess.run(['git', f'--git-dir={path}/{folder}/.git', 'log', '--graph', "--pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr)%Creset'", '--abbrev-commit', '--date=relative', 'master..origin/master'], text=True, capture_output=True)
    return commit.stdout

class MyDaemon(Daemon):
    def run(self):
        Notify.init("MyDaemon")
        time.sleep(1)
        Notify.Notification.new("run").show()
        folders = [folder for folder in os.listdir(path) if os.path.isdir(f'{path}/{folder}')]
        while True:
            for folder in folders:
                output = checkCommit(folder)
                if output:
                    Notify.Notification.new(f'folder: {folder}',output).show()            
            time.sleep(10)        

daemon = MyDaemon('/home/student/daemon-python/deamon.pid') 

if sys.argv[1] == "start":
    logging.info('start')
    daemon.start()    
elif sys.argv[1] == "stop":
    daemon.stop()    
elif sys.argv[1] == "restart":
    daemon.restart()
else:
    Notify.Notification.new("arguments error: no find argument\nenter someone argument\nstart\nstop\nrestart").show()
    sys.exit()