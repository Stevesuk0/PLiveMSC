import psutil
import os

"""
获取所有进程
"""
def get():
    #获取当前所有的进程
    return psutil.pids()

"""
    通过进程名判断该进程是否存在
"""
def search(processname):
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == processname:
            return True
    else:
        return False

"""
    通过进程名杀死进程
    taskkill /F /IM explorer.exe
"""
def kill(name):
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == name:
            cmd = r'taskkill /t /f /im '+ name
            os.system(cmd)

"""
通过进程名启动一个进程
"""
def run(name):
    os.system(name)