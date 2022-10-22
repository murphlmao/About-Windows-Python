import os, platform, winreg
from winreg import *


# Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\
# Display Name
# Ignore all keys that don't have DisplayName key
 
aKey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

class Sort_SoftwareRegKeys:
    def __init__(self, hi):
        self.hi = hi
        print(aKey, aReg)

    def Check(self):
        try:
            i = 0
            while 1:
                name, value, type = EnumValue(aReg, i)
                print(name, value, i)
                i += 1
        except WindowsError:
            print()
x = Sort_SoftwareRegKeys.Check()
