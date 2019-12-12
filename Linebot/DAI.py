import time, random, requests
import DAN

#ServerURL = 'http://IP:9999'      #with non-secure connection
ServerURL = 'https://6.iottalk.tw' #with SSL connection
Reg_addr = 'hank230201' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='hank_linebot'
DAN.profile['df_list']=['MSG-I', 'MSG-O',]
#DAN.profile['d_name']= 'Assign a Device Name' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line
temp=0
while True:
    try:
        IDF_data = random.uniform(1, 10)
        DAN.push ('MSG_I', IDF_data) #Push data to an input device feature "Dummy_Sensor"

        #==================================

        ODF_data = DAN.pull('MSG_O')#Pull data from an output device feature "Dummy_Control"
        
        if ODF_data != None:
            if ODF_data[0]!=temp:
                print (ODF_data[0])
                temp=ODF_data[0]
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)

