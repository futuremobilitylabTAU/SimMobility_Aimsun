import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from pandas import DataFrame
import random
import datetime
import uuid
import math
import utm


path_das=r'C:\Users\ASUS\Desktop\Thesis_AMOD\assets\cluster_and_anlysis\activity_schedule\Das'
path_centroid_circle=r'C:\Users\ASUS\Desktop\Thesis_AMOD\assets\cluster_and_anlysis\section_coordination_by_taz\ket_cord_filterd.csv'

## Save the result
outputs_folder=r'C:\Users\ASUS\Desktop\Thesis_AMOD\assets\cluster_and_anlysis\amod_schedule\requst.json'

#%%% In
simulation_year=2022
simulation_mounth=5
simulation_day=18
start_time=6.25
end_time=10.75

## randomal point from centroid center in origin and dest (in meters) (max) 
#radius=250

#%% Filter
das = pd.read_csv(path_das)
das = das[das['stop_mode']=='Taxi']
das = das[['person_id','stop_zone','stop_mode','stop_type','prev_stop_zone','prev_stop_departure_time']]
das=das[(das['prev_stop_departure_time']>=start_time)&(das['prev_stop_departure_time']<=end_time)]
das = das[das['stop_zone'].isin([41,42,43])==False]
das = das[das['prev_stop_zone'].isin([41,42,43])==False]
das = das[das['stop_zone'].isin([41,42,43])==False]

das=das[das['stop_zone']!=das['prev_stop_zone']]
#%% Person Type

das['person_type']="Type2CurrentModeNonCar"
#%% Epoch 

das['req_time']=das.apply(lambda x:  datetime.datetime(simulation_year,simulation_mounth,simulation_day,int(x['prev_stop_departure_time']),int(random.random() * (60 - 30) + 30),int(random.random()*60)).timestamp()*1000 if (x['prev_stop_departure_time']-int(x['prev_stop_departure_time']))==0.75
                      else datetime.datetime(simulation_year,simulation_mounth,simulation_day,int(x['prev_stop_departure_time']),int(random.random() * (30 - 0) + 0),int(random.random()*60)).timestamp()*1000  , axis=1)
#%% String Filds

das=das.sort_values(by='req_time', ascending=True)
das=das.reset_index()
das=das.reset_index()
das['req_name']=das.apply(lambda x:'Request'+' '+str(x['level_0']+1)+'('+str(x['prev_stop_zone'])+','+str(x['stop_zone'])+')',axis=1)
#%% Uniq Value

das['req_id']=das.apply(lambda x:str(uuid.uuid4()),axis=1)
#%% Ranndom Circle Point
centroid_circle=pd.read_csv(path_centroid_circle)


#%%%




#%%


das['or']=das.apply(lambda x:centroid_circle[centroid_circle['TAZV41']==x['prev_stop_zone']].sample()[['X','Y']],axis=1)
das['des']=das.apply(lambda x:centroid_circle[centroid_circle['TAZV41']==x['stop_zone']].sample()[['X','Y']],axis=1)


#%%
das['x_y_random_origins']=das.apply(lambda x: {'x':float(x['or']['X']),'y':float(x['or']['Y'])},axis=1)
das['x_y_random_dest']=das.apply(lambda x: {'x':float(x['des']['X']),'y':float(x['des']['Y'])},axis=1)



#%%% Ranndom Circle Point -Cancoulation

#das['random_angale_1']=das.apply(lambda x: random.random(),axis=1)
#das['random_readius_1']=das.apply(lambda x: random.random(),axis=1)
#das['random_angale_2']=das.apply(lambda x: random.random(),axis=1)
#das['random_readius_2']=das.apply(lambda x: random.random(),axis=1)

#das['x_y_random_origins']=das.apply(lambda x: {'x':(radius*x['random_readius_1'])*math.cos(2*math.pi*x['random_angale_1'])+x['X_x'],'y':(radius*x['random_readius_1'])*math.sin(2*math.pi* x['random_angale_1'])+x['Y_x']},axis=1)
#das['x_y_random_dest']=das.apply(lambda x: {'x':(radius*x['random_readius_2'])*math.cos(2*math.pi*x['random_angale_2'])+x['X_y'],'y':(radius*x['random_readius_2'])*math.sin(2*math.pi* x['random_angale_2'])+x['Y_y']},axis=1)
#das=das.drop(['random_angale_1','random_angale_2','random_angale_1','random_angale_2'],axis=1)

#das['dis_or']=das.apply(lambda x:math.sqrt((x['x_y_random_origins']['x']-x['X_x'])*(x['x_y_random_origins']['x']-x['X_x'])+(x['x_y_random_origins']['y']-x['Y_x'])*(x['x_y_random_origins']['y']-x['Y_x'])),axis=1)
#das['dis_de']=das.apply(lambda x:math.sqrt((x['x_y_random_dest']['x']-x['X_y'])*(x['x_y_random_dest']['x']-x['X_y'])+(x['x_y_random_dest']['y']-x['Y_y'])*(x['x_y_random_dest']['y']-x['Y_y'])),axis=1)

#%% Class For Json Object

class Out:
    def __init__(self, time,idd,name,person_type,req_purpose,origin,destination):
        
        self.time =time
        self.id =idd
        self.name =name
        self.person_type =person_type
        self.req_purpose =req_purpose
        self.origin ={'x':origin['x'],'y':origin['y']}
        self.destination ={'x':destination['x'],'y':destination['y']}

          
    def to_dict(self):    
        return {"time": self.time,"id": self.id,"name": self.name,"person_type": self.person_type,"req_purpose": self.req_purpose, "origin": {'x':self.origin['x'],'y':self.origin['y']}, "destination": {'x':self.destination['x'],'y':self.destination['y']}}
#%%  Biuld Json From Class

das['out object']=das.apply(lambda x:Out(x['req_time'],x['req_id'],x['req_name'],x['person_type'],x['stop_type'],x['x_y_random_origins'],x['x_y_random_dest']) ,axis=1)
list_of_oupots=das['out object'].to_list()
results = [obj.to_dict() for obj in list_of_oupots]
jsdata = json.dumps(results,indent='\t', separators=(',', ': '))
with open(outputs_folder, "w") as outfile:
    outfile.write(jsdata)

