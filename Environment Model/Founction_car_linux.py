import pandas as pd
import numpy as np


print("Enter to Ex-File")

print("Load CSV Tables")



########home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing/DataBase


path_co2=r"/home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing/DataBase/CO_2_table.csv"


path_nox=r"/home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing/DataBase/Nox_table.csv"


path_pm=r"/home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing/DataBase/PM_table.csv"


path_pm_shika=r"/home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing/DataBase/PM_Shika_table.csv"


path_nmvoc=r"/home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing/DataBase/NMVOC_table.csv"


path_nmvoc_ev=r"/home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing/DataBase/NMVOC_Ev_table.csv"


path_fc=r"/home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing/DataBase/FC_table.csv"



print("Load Values")

havy=12
stop_and_go=30
tp=19
############# written by gabriel dadashev start in 26.11.21 to 21.12.21

def make_co2_by_tables(d_list,c_list,v_list,speed_limit,road_type,L):


    
    CO2_list=[]
    co2_factors_table_orginal=pd.read_csv(path_co2,header='infer')

    for i in range(tp):
###########################Motorway#######################
     
           co2_factors_table=co2_factors_table_orginal.copy()
           if road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=havy:
                   co2_factors_table=co2_factors_table[['% CAR','COLD','90-Motorway - City- Freeflow']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['90-Motorway - City- Freeflow']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[1][0]<=havy:
                   co2_factors_table=co2_factors_table[['% CAR','COLD','80-Motorway - City- Freeflow']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['80-Motorway - City- Freeflow']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[1][0]<=havy:
                   co2_factors_table=co2_factors_table[['% CAR','COLD','70-Motorway - City- Freeflow']] 
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['70-Motorway - City- Freeflow']*L+co2_factors_table['COLD']*L)
                   
                   
           elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','90-Motorway - City-Heavy']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['90-Motorway - City-Heavy']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   co2_factors_table=co2_factors_table[['% CAR','COLD','80-Motorway - City-Heavy']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['80-Motorway - City-Heavy']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   co2_factors_table=co2_factors_table[['% CAR','COLD','70-Motorway - City-Heavy']] 
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['70-Motorway - City-Heavy']*L +co2_factors_table['COLD']*L)
                   
                   
           elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]>stop_and_go  :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','90-Motorway - City- Stop & Go']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['90-Motorway - City- Stop & Go']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]>stop_and_go :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','80-Motorway - City- Stop & Go']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['80-Motorway - City- Stop & Go']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]>stop_and_go :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','70-Motorway - City- Stop & Go']] 
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['70-Motorway - City- Stop & Go']*L +co2_factors_table['COLD']*L)

        ###########################"Primary","Secondary"#######################
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=havy  :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','50-Distributor / Secondary- Freeflow']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['50-Distributor / Secondary- Freeflow']*L+co2_factors_table['COLD']*L)
                     
    
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=havy  :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','60-Distributor / Secondary- Freeflow']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['60-Distributor / Secondary- Freeflow']*L+co2_factors_table['COLD']*L)
                   
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=havy:
                   co2_factors_table=co2_factors_table[['% CAR','COLD','70-Distributor / Secondary- Freeflow']] 
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['70-Distributor / Secondary- Freeflow']*L +co2_factors_table['COLD']*L)
       
        
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy  :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','50-Distributor / Secondary- Heavy']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['50-Distributor / Secondary- Heavy']*L+co2_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','60-Distributor / Secondary- Heavy']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['60-Distributor / Secondary- Heavy']*L+co2_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','70-Distributor / Secondary- Heavy']] 
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['70-Distributor / Secondary- Heavy']*L +co2_factors_table['COLD']*L)
        
        
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]>stop_and_go  :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','50-Distributor / Secondary- Stop & Go']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['50-Distributor / Secondary- Stop & Go']*L+co2_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]>stop_and_go :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','60-Distributor / Secondary- Stop & Go']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['60-Distributor / Secondary- Stop & Go']*L+co2_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]>stop_and_go :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','70-Distributor / Secondary- Stop & Go']] 
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['70-Distributor / Secondary- Stop & Go']*L +co2_factors_table['COLD']*L)
           
            
           ###########################                            Residential                       #################################3333
            
            
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=havy  :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','30-Access Residential-Freeflow']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['30-Access Residential-Freeflow']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=havy :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','40-Access Residential-Freeflow']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['40-Access Residential-Freeflow']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=havy :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','50-Access Residential-Freeflow']] 
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['50-Access Residential-Freeflow']*L +co2_factors_table['COLD']*L)
                   
                   
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','30-Access Residential-Heavy']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['30-Access Residential-Heavy']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   co2_factors_table=co2_factors_table[['% CAR','COLD','40-Access Residential-Heavy']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['40-Access Residential-Heavy']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   co2_factors_table=co2_factors_table[['% CAR','COLD','50-Access Residential-Heavy']] 
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['50-Access Residential-Heavy']*L  +co2_factors_table['COLD']*L)   
                   
                   
                   
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]>stop_and_go  :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','30-Access Residential- Stop & Go']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['30-Access Residential- Stop & Go']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]>stop_and_go :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','40-Access Residential- Stop & Go']]
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['40-Access Residential- Stop & Go']*L+co2_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]>stop_and_go :
                   co2_factors_table=co2_factors_table[['% CAR','COLD','50-Access Residential- Stop & Go']] 
                   co2_factors_table['em']=co2_factors_table['% CAR']*c_list[i][0]*(co2_factors_table['50-Access Residential- Stop & Go']*L   +co2_factors_table['COLD']*L)      
         
           else  :
                co2_factors_table['em']=0
          
     
           CO2_list.append(round(co2_factors_table['em'].sum(),2))                 
           
               
    return CO2_list



########################## founction 2 NOX ####################################



def make_nox_by_tables(d_list,c_list,v_list,speed_limit,road_type,L):
    
    Nox_list=[]
    nox_factors_table_orginal=pd.read_csv(path_nox,header='infer')

    for i in range(tp):
###########################Motorway#######################
     
           nox_factors_table=nox_factors_table_orginal.copy()
           if road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=havy:
                   nox_factors_table=nox_factors_table[['% CAR','COLD','90-Motorway - City- Freeflow']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['90-Motorway - City- Freeflow']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[1][0]<=havy:
                   nox_factors_table=nox_factors_table[['% CAR','COLD','80-Motorway - City- Freeflow']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['80-Motorway - City- Freeflow']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[1][0]<=havy:
                   nox_factors_table=nox_factors_table[['% CAR','COLD','70-Motorway - City- Freeflow']] 
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['70-Motorway - City- Freeflow']*L+nox_factors_table['COLD']*L)
                   
                   
           elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','90-Motorway - City-Heavy']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['90-Motorway - City-Heavy']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   nox_factors_table=nox_factors_table[['% CAR','COLD','80-Motorway - City-Heavy']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['80-Motorway - City-Heavy']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   nox_factors_table=nox_factors_table[['% CAR','COLD','70-Motorway - City-Heavy']] 
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['70-Motorway - City-Heavy']*L +nox_factors_table['COLD']*L)
                   
                   
           elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]>stop_and_go  :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','90-Motorway - City- Stop & Go']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['90-Motorway - City- Stop & Go']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]>stop_and_go :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','80-Motorway - City- Stop & Go']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['80-Motorway - City- Stop & Go']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]>stop_and_go :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','70-Motorway - City- Stop & Go']] 
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['70-Motorway - City- Stop & Go']*L +nox_factors_table['COLD']*L)

        ###########################"Primary","Secondary"#######################
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=havy  :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','50-Distributor / Secondary- Freeflow']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['50-Distributor / Secondary- Freeflow']*L+nox_factors_table['COLD']*L)
                     
    
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=havy  :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','60-Distributor / Secondary- Freeflow']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['60-Distributor / Secondary- Freeflow']*L+nox_factors_table['COLD']*L)
                   
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=havy:
                   nox_factors_table=nox_factors_table[['% CAR','COLD','70-Distributor / Secondary- Freeflow']] 
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['70-Distributor / Secondary- Freeflow']*L+nox_factors_table['COLD']*L) 
       
        
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy  :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','50-Distributor / Secondary- Heavy']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['50-Distributor / Secondary- Heavy']*L+nox_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','60-Distributor / Secondary- Heavy']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['60-Distributor / Secondary- Heavy']*L+nox_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','70-Distributor / Secondary- Heavy']] 
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['70-Distributor / Secondary- Heavy']*L +nox_factors_table['COLD']*L)
        
        
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]>stop_and_go  :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','50-Distributor / Secondary- Stop & Go']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['50-Distributor / Secondary- Stop & Go']*L+nox_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]>stop_and_go :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','60-Distributor / Secondary- Stop & Go']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['60-Distributor / Secondary- Stop & Go']*L+nox_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]>stop_and_go :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','70-Distributor / Secondary- Stop & Go']] 
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['70-Distributor / Secondary- Stop & Go']*L +nox_factors_table['COLD']*L)
           
            
           ###########################                            Residential                       #################################3333
            
            
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=havy  :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','30-Access Residential-Freeflow']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['30-Access Residential-Freeflow']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=havy :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','40-Access Residential-Freeflow']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['40-Access Residential-Freeflow']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=havy :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','50-Access Residential-Freeflow']] 
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['50-Access Residential-Freeflow']*L +nox_factors_table['COLD']*L)
                   
                   
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','30-Access Residential-Heavy']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['30-Access Residential-Heavy']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   nox_factors_table=nox_factors_table[['% CAR','COLD','40-Access Residential-Heavy']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['40-Access Residential-Heavy']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   nox_factors_table=nox_factors_table[['% CAR','COLD','50-Access Residential-Heavy']] 
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['50-Access Residential-Heavy']*L +nox_factors_table['COLD']*L)    
                   
                   
                   
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]>stop_and_go  :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','30-Access Residential- Stop & Go']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['30-Access Residential- Stop & Go']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]>stop_and_go :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','40-Access Residential- Stop & Go']]
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['40-Access Residential- Stop & Go']*L+nox_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]>stop_and_go :
                   nox_factors_table=nox_factors_table[['% CAR','COLD','50-Access Residential- Stop & Go']] 
                   nox_factors_table['em']=nox_factors_table['% CAR']*c_list[i][0]*(nox_factors_table['50-Access Residential- Stop & Go']*L +nox_factors_table['COLD']*L)        
         
           else  :
                nox_factors_table['em']=0
          
     
           Nox_list.append(round(nox_factors_table['em'].sum(),2))                 
           
               
    return Nox_list



def make_pm_by_tables(d_list,c_list,v_list,speed_limit,road_type,L):
    
    PM_list=[]
    pm_factors_table_orginal=pd.read_csv(path_pm,header='infer')
    pm_ab_em=pd.read_csv(path_pm_shika,header='infer')
    pm_ab_em=pm_ab_em.set_index('Type') ##### Plitot idioy


    for i in range(tp):
###########################Motorway#######################
     
           pm_factors_table=pm_factors_table_orginal.copy()
           if road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=havy:
                   pm_factors_table=pm_factors_table[['% CAR','COLD','90-Motorway - City- Freeflow']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['90-Motorway - City- Freeflow']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[1][0]<=havy:
                   pm_factors_table=pm_factors_table[['% CAR','COLD','80-Motorway - City- Freeflow']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['80-Motorway - City- Freeflow']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[1][0]<=havy:
                   pm_factors_table=pm_factors_table[['% CAR','COLD','70-Motorway - City- Freeflow']] 
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['70-Motorway - City- Freeflow']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
                   
                   
           elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','90-Motorway - City-Heavy']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['90-Motorway - City-Heavy']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   pm_factors_table=pm_factors_table[['% CAR','COLD','80-Motorway - City-Heavy']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['80-Motorway - City-Heavy']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   pm_factors_table=pm_factors_table[['% CAR','COLD','70-Motorway - City-Heavy']] 
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['70-Motorway - City-Heavy']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L) 
                   
                   
           elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]>stop_and_go  :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','90-Motorway - City- Stop & Go']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['90-Motorway - City- Stop & Go']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]>stop_and_go :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','80-Motorway - City- Stop & Go']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['80-Motorway - City- Stop & Go']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]>stop_and_go :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','70-Motorway - City- Stop & Go']] 
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['70-Motorway - City- Stop & Go']*L +pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)

        ###########################"Primary","Secondary"#######################
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=havy  :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','50-Distributor / Secondary- Freeflow']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['50-Distributor / Secondary- Freeflow']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
                     
    
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=havy  :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','60-Distributor / Secondary- Freeflow']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['60-Distributor / Secondary- Freeflow']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
                   
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=havy:
                   pm_factors_table=pm_factors_table[['% CAR','COLD','70-Distributor / Secondary- Freeflow']] 
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['70-Distributor / Secondary- Freeflow']*L +pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
       
        
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy  :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','50-Distributor / Secondary- Heavy']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['50-Distributor / Secondary- Heavy']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','60-Distributor / Secondary- Heavy']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['60-Distributor / Secondary- Heavy']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','70-Distributor / Secondary- Heavy']] 
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['70-Distributor / Secondary- Heavy']*L +pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
        
        
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]>stop_and_go  :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','50-Distributor / Secondary- Stop & Go']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['50-Distributor / Secondary- Stop & Go']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]>stop_and_go :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','60-Distributor / Secondary- Stop & Go']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['60-Distributor / Secondary- Stop & Go']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]>stop_and_go :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','70-Distributor / Secondary- Stop & Go']] 
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['70-Distributor / Secondary- Stop & Go']*L +pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           
            
           ###########################                            Residential                       #################################3333
            
            
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=havy  :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','30-Access Residential-Freeflow']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['30-Access Residential-Freeflow']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=havy :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','40-Access Residential-Freeflow']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['40-Access Residential-Freeflow']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=havy :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','50-Access Residential-Freeflow']] 
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['50-Access Residential-Freeflow']*L +pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
                   
                   
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','30-Access Residential-Heavy']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['30-Access Residential-Heavy']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   pm_factors_table=pm_factors_table[['% CAR','COLD','40-Access Residential-Heavy']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['40-Access Residential-Heavy']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   pm_factors_table=pm_factors_table[['% CAR','COLD','50-Access Residential-Heavy']] 
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['50-Access Residential-Heavy']*L  +pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)   
                   
                   
                   
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]>stop_and_go  :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','30-Access Residential- Stop & Go']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['30-Access Residential- Stop & Go']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]>stop_and_go :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','40-Access Residential- Stop & Go']]
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['40-Access Residential- Stop & Go']*L+pm_factors_table['COLD']*L+pm_ab_em.loc['Car','Total']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]>stop_and_go :
                   pm_factors_table=pm_factors_table[['% CAR','COLD','50-Access Residential- Stop & Go']] 
                   pm_factors_table['em']=pm_factors_table['% CAR']*c_list[i][0]*(pm_factors_table['50-Access Residential- Stop & Go']*L +pm_factors_table['COLD']*L +pm_ab_em.loc['Car','Total']*L)      
         
           else  :
                pm_factors_table['em']=0
          
     
           PM_list.append(round(pm_factors_table['em'].sum(),2))                 
           
               
    return PM_list




def make_voc_by_tables(d_list,c_list,v_list,speed_limit,road_type,L):
    
    MVOC_list=[]
    mvoc_factors_table_orginal=pd.read_csv(path_nmvoc,header='infer')
    mvoc_ev_em=pd.read_csv(path_nmvoc_ev,header='infer')
    mvoc_ev_em=mvoc_ev_em.set_index('Type') ##### Plitot idioy


    for i in range(tp):
###########################Motorway#######################
     
           mvoc_factors_table=mvoc_factors_table_orginal.copy()
           if road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=havy:
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','90-Motorway - City- Freeflow']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['90-Motorway - City- Freeflow']*L+mvoc_ev_em.loc['Car','Highway']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[1][0]<=havy:
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','80-Motorway - City- Freeflow']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['80-Motorway - City- Freeflow']*L+mvoc_ev_em.loc['Car','Highway']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[1][0]<=havy:
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','70-Motorway - City- Freeflow']] 
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['70-Motorway - City- Freeflow']*L+mvoc_ev_em.loc['Car','Highway']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
                   
                   
           elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','90-Motorway - City-Heavy']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['90-Motorway - City-Heavy']*L+mvoc_ev_em.loc['Car','Highway']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','80-Motorway - City-Heavy']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['80-Motorway - City-Heavy']*L+mvoc_ev_em.loc['Car','Highway']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','70-Motorway - City-Heavy']] 
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['70-Motorway - City-Heavy']*L +mvoc_ev_em.loc['Car','Highway']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
                   
                   
           elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]>stop_and_go  :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','90-Motorway - City- Stop & Go']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['90-Motorway - City- Stop & Go']*L+mvoc_ev_em.loc['Car','Highway']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]>stop_and_go :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','80-Motorway - City- Stop & Go']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['80-Motorway - City- Stop & Go']*L+mvoc_ev_em.loc['Car','Highway']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]>stop_and_go :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','70-Motorway - City- Stop & Go']] 
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['70-Motorway - City- Stop & Go']*L +mvoc_ev_em.loc['Car','Highway']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)

        ###########################"Primary","Secondary"#######################
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=havy  :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','50-Distributor / Secondary- Freeflow']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['50-Distributor / Secondary- Freeflow']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
                     
    
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=havy  :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','60-Distributor / Secondary- Freeflow']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['60-Distributor / Secondary- Freeflow']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
                   
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=havy:
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','70-Distributor / Secondary- Freeflow']] 
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['70-Distributor / Secondary- Freeflow']*L +mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
       
        
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy  :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','50-Distributor / Secondary- Heavy']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['50-Distributor / Secondary- Heavy']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','60-Distributor / Secondary- Heavy']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['60-Distributor / Secondary- Heavy']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','70-Distributor / Secondary- Heavy']] 
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['70-Distributor / Secondary- Heavy']*L +mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
        
        
           elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]>stop_and_go  :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','50-Distributor / Secondary- Stop & Go']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['50-Distributor / Secondary- Stop & Go']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]>stop_and_go :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','60-Distributor / Secondary- Stop & Go']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['60-Distributor / Secondary- Stop & Go']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]>stop_and_go :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','70-Distributor / Secondary- Stop & Go']] 
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['70-Distributor / Secondary- Stop & Go']*L +mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           
            
           ###########################                            Residential                       #################################3333
            
            
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=havy  :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','30-Access Residential-Freeflow']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['30-Access Residential-Freeflow']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=havy :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','40-Access Residential-Freeflow']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['40-Access Residential-Freeflow']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=havy :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','50-Access Residential-Freeflow']] 
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['50-Access Residential-Freeflow']*L +mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
                   
                   
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','30-Access Residential-Heavy']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['30-Access Residential-Heavy']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','40-Access Residential-Heavy']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['40-Access Residential-Heavy']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','50-Access Residential-Heavy']] 
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['50-Access Residential-Heavy']*L  +mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)   
                   
                   
                   
           elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]>stop_and_go  :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','30-Access Residential- Stop & Go']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['30-Access Residential- Stop & Go']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]>stop_and_go :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','40-Access Residential- Stop & Go']]
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['40-Access Residential- Stop & Go']*L+mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const']+mvoc_factors_table['COLD']*L)
           elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]>stop_and_go :
                   mvoc_factors_table=mvoc_factors_table[['% CAR','COLD','50-Access Residential- Stop & Go']] 
                   mvoc_factors_table['em']=mvoc_factors_table['% CAR']*c_list[i][0]*(mvoc_factors_table['50-Access Residential- Stop & Go']*L +mvoc_ev_em.loc['Car','Urban']*L+mvoc_ev_em.loc['Car','Diurnal-Const'] +mvoc_factors_table['COLD']*L)    
         
           else  :
                mvoc_factors_table['em']=0
          
     
           MVOC_list.append(round(mvoc_factors_table['em'].sum()+mvoc_ev_em.loc['Car','Diurnal-Const']*c_list[i][0],2))                 
           
               
    return MVOC_list



def make_fc_by_tables(d_list,c_list,v_list,speed_limit,road_type,L):
    
    
    fc_list=[]
    fc_factors_table_orginal=pd.read_csv(path_fc,header='infer')
    for i in range(tp):
        
###########################Motorway#######################
     
        fc_factors_table=fc_factors_table_orginal.copy()
        if road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=havy:
            
            fc_factors_table=fc_factors_table[['% CAR','90-Motorway - City- Freeflow']]
            fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['90-Motorway - City- Freeflow']*L
        elif  road_type=='Motorway' and speed_limit==80 and d_list[1][0]<=havy:
                   fc_factors_table=fc_factors_table[['% CAR','80-Motorway - City- Freeflow']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['80-Motorway - City- Freeflow']*L
        elif  road_type=='Motorway' and speed_limit==70 and d_list[1][0]<=havy:
                   fc_factors_table=fc_factors_table[['% CAR','70-Motorway - City- Freeflow']] 
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['70-Motorway - City- Freeflow']*L
                   
                   
        elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   fc_factors_table=fc_factors_table[['% CAR','90-Motorway - City-Heavy']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['90-Motorway - City-Heavy']*L
        elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   fc_factors_table=fc_factors_table[['% CAR','80-Motorway - City-Heavy']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['80-Motorway - City-Heavy']*L
        elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   fc_factors_table=fc_factors_table[['% CAR','70-Motorway - City-Heavy']] 
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['70-Motorway - City-Heavy']*L 
                   
                   
        elif  road_type=='Motorway' and speed_limit==90 and d_list[i][0]>stop_and_go  :
                   fc_factors_table=fc_factors_table[['% CAR','90-Motorway - City- Stop & Go']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['90-Motorway - City- Stop & Go']*L
        elif  road_type=='Motorway' and speed_limit==80 and d_list[i][0]>stop_and_go :
                   fc_factors_table=fc_factors_table[['% CAR','80-Motorway - City- Stop & Go']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['80-Motorway - City- Stop & Go']*L
        elif  road_type=='Motorway' and speed_limit==70 and d_list[i][0]>stop_and_go :
                   fc_factors_table=fc_factors_table[['% CAR','70-Motorway - City- Stop & Go']] 
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['70-Motorway - City- Stop & Go']*L 

        ###########################"Primary","Secondary"#######################
        elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=havy  :
                   fc_factors_table=fc_factors_table[['% CAR','50-Distributor / Secondary- Freeflow']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['50-Distributor / Secondary- Freeflow']*L
                     
    
        elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=havy  :
                   fc_factors_table=fc_factors_table[['% CAR','60-Distributor / Secondary- Freeflow']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['60-Distributor / Secondary- Freeflow']*L
                   
        elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=havy:
                   fc_factors_table=fc_factors_table[['% CAR','70-Distributor / Secondary- Freeflow']] 
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['70-Distributor / Secondary- Freeflow']*L 
       
        
        elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy  :
                   fc_factors_table=fc_factors_table[['% CAR','50-Distributor / Secondary- Heavy']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['50-Distributor / Secondary- Heavy']*L
        elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   fc_factors_table=fc_factors_table[['% CAR','60-Distributor / Secondary- Heavy']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['60-Distributor / Secondary- Heavy']*L
        elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   fc_factors_table=fc_factors_table[['% CAR','70-Distributor / Secondary- Heavy']] 
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['70-Distributor / Secondary- Heavy']*L 
        
        
        elif  road_type  in ("Primary","Secondary") and speed_limit==50 and d_list[i][0]>stop_and_go  :
                   fc_factors_table=fc_factors_table[['% CAR','50-Distributor / Secondary- Stop & Go']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['50-Distributor / Secondary- Stop & Go']*L
        elif  road_type  in ("Primary","Secondary") and speed_limit==60 and d_list[i][0]>stop_and_go :
                   fc_factors_table=fc_factors_table[['% CAR','60-Distributor / Secondary- Stop & Go']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['60-Distributor / Secondary- Stop & Go']*L
        elif  road_type  in ("Primary","Secondary") and speed_limit==70 and d_list[i][0]>stop_and_go :
                   fc_factors_table=fc_factors_table[['% CAR','70-Distributor / Secondary- Stop & Go']] 
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['70-Distributor / Secondary- Stop & Go']*L 
           
            
           ###########################                            Residential                       #################################3333
            
            
        elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=havy  :
                   fc_factors_table=fc_factors_table[['% CAR','30-Access Residential-Freeflow']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['30-Access Residential-Freeflow']*L
        elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=havy :
                   fc_factors_table=fc_factors_table[['% CAR','40-Access Residential-Freeflow']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['40-Access Residential-Freeflow']*L
        elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=havy :
                   fc_factors_table=fc_factors_table[['% CAR','50-Access Residential-Freeflow']] 
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['50-Access Residential-Freeflow']*L 
                   
                   
        elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy :
                   fc_factors_table=fc_factors_table[['% CAR','30-Access Residential-Heavy']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['30-Access Residential-Heavy']*L
        elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   fc_factors_table=fc_factors_table[['% CAR','40-Access Residential-Heavy']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['40-Access Residential-Heavy']*L
        elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]<=stop_and_go and d_list[i][0]>havy:
                   fc_factors_table=fc_factors_table[['% CAR','50-Access Residential-Heavy']] 
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['50-Access Residential-Heavy']*L     
                   
                   
                   
        elif  road_type=='Residential' and speed_limit==30 and d_list[i][0]>stop_and_go  :
                   fc_factors_table=fc_factors_table[['% CAR','30-Access Residential- Stop & Go']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['30-Access Residential- Stop & Go']*L
        elif  road_type=='Residential' and speed_limit==40 and d_list[i][0]>stop_and_go :
                   fc_factors_table=fc_factors_table[['% CAR','40-Access Residential- Stop & Go']]
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['40-Access Residential- Stop & Go']*L
        elif  road_type=='Residential' and speed_limit==50 and d_list[i][0]>stop_and_go :
                   fc_factors_table=fc_factors_table[['% CAR','50-Access Residential- Stop & Go']] 
                   fc_factors_table['em']=fc_factors_table['% CAR']*c_list[i][0]*fc_factors_table['50-Access Residential- Stop & Go']*L         
         
        else  :
                fc_factors_table['em']=0
          
     
        fc_list.append(round(fc_factors_table['em'].sum(),2))                 
           
               
    return fc_list
    



#a=[(0.29004266604555823, True), (17, True), (50, True), (6, True), (2.7744808911831638, True), (1.9227321443835161, True), (1.6794182125556532, True), (1.7923587760787347, True), (2.0035048109768776, True), (1.6043606800475314, True), (1.1017454220258036, True), (0.5288732458251398, True), (0.19425908365286512, True), (0.05269611079369435, True), (0.2739774848407997, True), (0.2350513104422155, True)]
#b=[(27.0, True), (106.0, True), (179.0, True), (289.0, True), (269.0, True), (184.0, True), (165.0, True), (173.0, True), (195.0, True), (158.0, True), (107.0, True), (53.0, True), (19.0, True), (5.0, True), (26.0, True), (24.0, True)]
#c=[(100.15242555371688, True), (98.87021730144795, True), (96.66301050690245, True), (97.6351167142102, True), (97.39319999309399, True), (96.57559568810832, True), (97.88893047097234, True), (97.65258084940048, True), (96.83790669157563, True), (99.53544975174093, True), (97.79255957312799, True), (98.75911623781832, True), (98.40496882954008, True), (95.77100734154271, True), (99.1819027097086, True), (98.33198433418418, True)]
#d=30
#r=5
#e='Residential'
#k=make_fc_by_tables(a,b,c,d,e,r)
#k1=make_co2_by_tables(a,b,c,d,e,r)
#print(k1)
#f=pd.read_csv(r"C:\Scripts\Python Docs\CO_2_table.csv",header='infer')
