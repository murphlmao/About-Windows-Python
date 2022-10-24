import winreg, psutil, pprint, os

pp = pprint.PrettyPrinter(depth=1)


# alphabetical ordurrrrr
def Alph_Order(e):
    return e['name']

# retreiving information from the registry
class Registry_Shit:
    def __init__(self) -> None:
        pass

    @staticmethod # dont need no 'self' botherin me
    def Software_RegistryKeys(hive, flag):
        aReg = winreg.ConnectRegistry(None, hive)
        aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | flag)
        count_subkey = winreg.QueryInfoKey(aKey)[0]
        software_list = []

        for i in range(count_subkey):
            software = {}
            try:
                asubkey_name = winreg.EnumKey(aKey, i)
                asubkey = winreg.OpenKey(aKey, asubkey_name)
                software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

                try:
                    software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
                except EnvironmentError:
                    software['version'] = 'undefined'

                try:
                    software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
                except EnvironmentError:
                    software['publisher'] = 'undefined'

                software_list.append(software)
            except EnvironmentError:
                continue
        return software_list

    @staticmethod
    def Network_RegistryKeys():
        # HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces
        inet_connections = psutil.net_if_addrs() # [0]
        inet_connections_keys = inet_connections.keys() # [1], keys only of key/value pair
        sign_remote = os.system("Set-ExecutionPolicy RemoteSigned")
        netsh_wlan_profiles = os.system("netsh wlan show profiles") # [2]


        return inet_connections, inet_connections_keys, netsh_wlan_profiles, sign_remote

    @staticmethod
    def Hardware_Utils():
        pass

    @staticmethod
    def Users_Utils():
        psutil.users()
        pass

class Printing_Shkabang: # printing class
    def __init__(self) -> None:
        # HKEY_LM_32 = SoftKeys(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY)
        # HKEY_LM_64 = SoftKeys(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
        # HKEY_CU_0 = SoftKeys(winreg.HKEY_CURRENT_USER, 0)
        # software block
        SoftKeys = Registry_Shit.Software_RegistryKeys
        self.HKEY_LM32 = SoftKeys(winreg.HKEY_CURRENT_USER, 0)
        self.HKEY_LM64 = SoftKeys(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
        self.HKEY_CU0 = SoftKeys(winreg.HKEY_CURRENT_USER, 0)
        
        # network block
        self.NetKeys = Registry_Shit.Network_RegistryKeys

    def list_softwareReg(self):
        software_list = self.HKEY_LM32 + self.HKEY_LM64 + self.HKEY_CU0 # array of dicts to find all established software in registry
        software_list.sort(key=Alph_Order) # alphabetical order bc easier to read lol
        software_file = open("exports\software_RegList.ini", "w") # export file // MAY BE A WAY TO PORT SOME OF THIS INTO A FUNCTION FOR AUTOMATION IN THE FUTURE
        driver_file = open("exports\driver_RegList.ini", "w") # export file 
        drivers_list = ["Intel(R)", "Python", "Runtime", "C++", "Driver", "Service"] # wordlist to distinguish drivers from actual software
        drivers_providers = ["Intel Corporation"] # providers/publishers for drivers. likely to be some edge cases

        for software in software_list:
            print(f"Name: {software['name']}\nVersion: {software['version']}\nPublisher: {software['publisher']}\n----------")

            if any(word in software['name'] for word in drivers_list):
                driver_file.write(f"[{software['name']}]\nName={software['name']}\nVersion={software['version']}\nPublisher={software['publisher']}\n\n")
    
            if any(word in software['publisher'] for word in drivers_providers):
               driver_file.write(f"[{software['name']}]\nName={software['name']}\nVersion={software['version']}\nPublisher={software['publisher']}\n\n")
            
            else:
                software_file.write(f"[{software['name']}]\nName={software['name']}\nVersion={software['version']}\nPublisher={software['publisher']}\n\n")
        
        print(f"Number of installed apps: {len(software_list)}")

    def list_networkReg(self):
        test_addr = self.NetKeys()
        pp.pprint(test_addr[0])

    def list_hardwareSpec(self):
        # psutils shit
        logical_processor_count = psutil.cpu_count()
        pass


if __name__ == "__main__":
    DoTheThing = Printing_Shkabang()

    DoTheThing.list_softwareReg()

    DoTheThing.list_networkReg()