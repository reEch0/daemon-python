#!/usr/bin/python3
import time
from deamon import Daemon
import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify
import subprocess
#from sys import argv
import sys
import os

COMMAND_LOG = "git log --graph --pretty==format:'%Cred%h%Creset - %C(yellow)%d%Creset %s %Cgreen(%cr)%Creset' --abbrev-commit --date=relative master..origin/master"
COMMAND_FETCH = "get fetch"

path_gir_dir1 = "home/kovalenko/git_dir1/test"


class MyDaemon(Daemon):
    def run(self):
        Notify.Notification.new("run").show()        
        #self.runBash(COMMAND_LOG)
        #self.checkCommit()

        file = open('home/kovalenko/example.txt','w+')
        file.write('checkCom')
        call_proc = subprocess.run('git',path_gir_dir1,'fetch')
        #file.write(call_proc)
        file.close()
        while True:
            time.sleep(1)

    def runBash(commandLine):                
        proc = subprocess.Popen(commandLine, shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read().strip()
        #file.write(out)
        return out
    def checkCommit():
        #file = open('example.txt','a+')
        #file.write('checkCom')
        call_proc = subprocess.run('git',path_gir_dir1,'fetch')
        #file.write(call_proc)
        #file.close()
        return 1
    
daemon = MyDaemon('/home/kovalenko/deamon.pid')
Notify.init("MyDaemon")
#try:
Notify.Notification.new(sys.argv[1]).show()
if sys.argv[1] == "start":
    daemon.start()
    #Notify.Notification.new("daemon start").show()
elif sys.argv[1] == "stop":
    daemon.stop()
    Notify.Notification.new("daemon stop").show()
elif sys.argv[1] == "restart":
    daemon.restart()
    Notify.Notification.new("daemon restart").show()
#except :
    #Notify.Notification.new("arguments error: no find argument\nenter someone argument\nstart\nstop\nrestart").show()
    #sys.exit()

#Notify.Notification.new("test notify").show()