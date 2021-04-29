import time, random, requests
import DAN

# ServerURL = 'http://demo.iottalk.tw:9999'      #with non-secure connection
ServerURL = 'http://140.114.77.75:9999/'
# ServerURL = 'https://demo.iottalk.tw' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address

# DAN.profile['dm_name']='Wash'
# DAN.profile['df_list']=['Status', 'Name-O']
DAN.profile['dm_name']='Dummy_Device'
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control']
#DAN.profile['d_name']= 'Assign a Device Name' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

while True:
    try:
        IDF_data = random.uniform(1, 10)
        # DAN.push ('Status', int(IDF_data)) #Push data to an input device feature "Dummy_Sensor"
        DAN.push ('Dummy_Sensor', int(IDF_data))
        #==================================

        # ODF_data = DAN.pull('Name-O')#Pull data from an output device feature "Dummy_Control"
        ODF_data = DAN.pull('Dummy_Control')
        if ODF_data != None:
            print (ODF_data[0])

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)