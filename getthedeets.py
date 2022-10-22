import winreg

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

class Printing_Shkabang: # printing class
    def __init__(self) -> None:
        # HKEY_LM_32 = SoftKeys(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY)
        # HKEY_LM_64 = SoftKeys(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
        # HKEY_CU_0 = SoftKeys(winreg.HKEY_CURRENT_USER, 0)
        SoftKeys = Registry_Shit.Software_RegistryKeys
        self.HKEY_LM32 = SoftKeys(winreg.HKEY_CURRENT_USER, 0)
        self.HKEY_LM64 = SoftKeys(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
        self.HKEY_CU0 = SoftKeys(winreg.HKEY_CURRENT_USER, 0)

    def list_software(self):
        software_list = self.HKEY_LM32 + self.HKEY_LM64 + self.HKEY_CU0 # array of dicts to find all established software in registry
        software_list.sort(key=Alph_Order) # alphabetical order bc easier to read lol
        software_file = open("software_RegList.ini", "w")
        driver_file = open("driver_RegList.ini", "w")
        drivers_list = ["Intel(R)", "Python", "Runtime", "C++", "Driver", "Service"]
        drivers_providers = ["Intel Corporation"]

        for software in software_list:
            print(f"Name: {software['name']}\nVersion: {software['version']}\nPublisher: {software['publisher']}\n----------")

            if any(word in software['name'] for word in drivers_list):
                driver_file.write(f"[{software['name']}]\nName={software['name']}\nVersion={software['version']}\nPublisher={software['publisher']}\n\n")
    
            if any(word in software['publisher'] for word in drivers_providers):
               driver_file.write(f"[{software['name']}]\nName={software['name']}\nVersion={software['version']}\nPublisher={software['publisher']}\n\n")
            
            else:
                software_file.write(f"[{software['name']}]\nName={software['name']}\nVersion={software['version']}\nPublisher={software['publisher']}\n\n")
        
        print(f"Number of installed apps: {len(software_list)}")

if __name__ == "__main__":
    DoTheThing = Printing_Shkabang()
    DoTheThing.list_software()