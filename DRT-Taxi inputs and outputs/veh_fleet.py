import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from pandas import DataFrame
import random
import datetime
import uuid
import math


#%%% In Data Location

### Key from Trafic Zones to City 
path_city_key=r'C:\Users\ASUS\Dropbox\Operating_Autonomous_Vehicles_in_Israel\SimulationforElectricEnergy\AMOD_from_taxi_simulation\DataBase Inputs\City_Key.csv'

### Israel Transportation Ministry Data
taxi=r'C:\Users\ASUS\Dropbox\Operating_Autonomous_Vehicles_in_Israel\SimulationforElectricEnergy\AMOD_from_taxi_simulation\DataBase Inputs\taxi_statictic.csv'

### Cordinant List on Road Section on the Supply Model by Trafic Zone
path_centroid_circle=r'C:\Users\ASUS\Dropbox\Operating_Autonomous_Vehicles_in_Israel\SimulationforElectricEnergy\AMOD_from_taxi_simulation\DataBase Inputs\ket_cord_filterd.csv'


## Save the result Location
outputs_folder=r'C:\Users\ASUS\Dropbox\Operating_Autonomous_Vehicles_in_Israel\SimulationforElectricEnergy\AMOD_from_taxi_simulation\veh_section_cord_2023.json'

## Tel Aviv Mero -Area Towns
list_of_cities=["OR YEHUDA","AZOR","ELISHAMA","BE'ER YA'AQOV","BET DAGAN","BENE BERAQ","BENE ATAROT","BAT YAM","GIV'AT SHEMU'EL","GIV'ATAYIM",'GANNE TIQWA',"HOD HASHARON","HERZLIYYA","HOLON","YAGEL","YEHUD","KEFAR SAVA","LOD","MAGSHIMIM","MISHMAR HASHIV'A","NES ZIYYONA","PETAH TIQWA","QIRYAT ONO","QIRYAT EQRON","RISHON LEZIYYON","REHOVOT","RAMLA","RAMAT GAN","RAMAT HASHARON","RA'ANNANA","TEL AVIV - YAFO"]

### JSON  Data for Aimsun Ride simulator
operator_id="c6b8efd5-0c03-438c-9a54-a81096a6bf97"
operator_name="DRT-Taxi operator"
ttype="external"
adress="localhost:45001"
aimsun_veh_number=18373060

#%%%%%%%%% Filter
city = pd.read_csv(path_city_key)
taxi_data = pd.read_csv(taxi)
taxi_data=taxi_data[taxi_data['City_Eng '].isin(list_of_cities)]

#%%%%%%%%% Expend Table By Value
fleet = taxi_data.loc[taxi_data.index.repeat(taxi_data['Taxi'])].assign(veh_id=0).reset_index(drop=True)

#%% veh id
fleet['veh_id']=fleet.apply(lambda x:str(uuid.uuid4()),axis=1)

#%%  Counter of Veh in the city and in all fleet
fleet=fleet.reset_index()
min_index=fleet.groupby('City_Eng ')['index'].min()
fleet=fleet.merge(min_index,left_on='City_Eng ',right_on=min_index.index,how='left')
fleet['veh_count']=fleet.index-fleet['index_y']+1
fleet=fleet.drop(['index_y'],axis=1)
fleet['index_x']=fleet['index_x']+1

fleet['name']=fleet.apply(lambda x:'VEH-'+str(x['veh_count'])+'-'+str(x['City_Eng '])+'-'+str(x['index_x']),axis=1)

#%% Randoum Taz for reach veh in city fleet
fleet['veh_taz']=fleet.apply(lambda x:int(city[city['Eng']==x['City_Eng ']].sample()['TAZ']),axis=1)

#%% Merge The Cordinants
fleet=fleet.merge(city[['TAZ', 'Centrioid-X', 'Centrioid-Y']],left_on='veh_taz',right_on='TAZ',how='left')

#%% Random Point on Roads of  City/Town

centroid_circle=pd.read_csv(path_centroid_circle)


a=fleet[fleet['veh_taz'].isin(centroid_circle['TAZV41'])==False]
b=a['veh_taz'].value_counts()

fleet['x_or']=fleet.apply(lambda x:float(centroid_circle[centroid_circle['TAZV41']==x['veh_taz']].sample()['X']),axis=1)
fleet['y_or']=fleet.apply(lambda x:float(centroid_circle[centroid_circle['TAZV41']==x['veh_taz']].sample()['Y']),axis=1)

fleet['x_y_random']=fleet.apply(lambda x: {'x':x['x_or'],'y':x['y_or']},axis=1)




#%% Class For Json Object

class Fleet:
    def __init__(self, idd,origin,name):
        
        self.id =idd
        self.origin ={'x':origin['x'],'y':origin['y']}
        self.name =name
         
    def to_dict(self):    
        return {"id": self.id, "origin": {'x':self.origin['x'],'y':self.origin['y']},"name": self.name}
#%%  Biuld Json

fleet['fleet object']=fleet.apply(lambda x:Fleet(x['veh_id'],x['x_y_random'],x['name']) ,axis=1)
list_of_oupots=fleet['fleet object'].to_list()
results = [obj.to_dict() for obj in list_of_oupots]
jsdata = json.dumps({"id": operator_id,"name": operator_name,"type": ttype,"address": adress,"vehicle_type": aimsun_veh_number,"fleet": results},indent='\t', separators=(',', ': '))

with open(outputs_folder, "w") as outfile:
    outfile.write(jsdata)


