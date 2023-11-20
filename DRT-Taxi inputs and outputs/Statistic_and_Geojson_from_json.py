import pandas as pd
import json
from pandas import json_normalize
from datetime import datetime
import utm
from pyproj import Transformer

#%% Tables Making from-Json

outputs=r'C:\Users\ASUS\Desktop\out.json'

###save location
geojson_req=r'C:\Users\ASUS\Desktop\gabi_to_req_full.json'
geojson_dest=r'C:\Users\ASUS\Desktop\gabi_to_dest_full.json'
req=r'C:\Users\ASUS\Desktop\req_full.csv'
trips_to_dest=r'C:\Users\ASUS\Desktop\trips_to_dest_full.csv'
trips_to_req=r'C:\Users\ASUS\Desktop\trips_to_req_full.csv'
stat1=r'C:\Users\ASUS\Desktop\stat_full.csv'
all_veh_events=r'C:\Users\ASUS\Desktop\veh_event.csv'





with open(outputs, 'r') as file:
    data = file.read().replace('\n', '')
    
dict= json.loads(data)
del data 
events = json_normalize(dict['events']) 


#utm.to_latlon(180610, 657248, 36, 'R')

#%%%   Time Convert from Epoh

events['time']=(events['time']/1000)
events['time'] = events['time'].apply(lambda x:datetime.fromtimestamp(x))
events['time'] = events['time'].apply(lambda x:x.strftime('%H:%M:%S'))

#%% Clean Table

events=events.drop([ 'operator','utility_data.Distance.coef', 'utility_data.Distance.offer','utility_data.Error.coef', 'utility_data.Error.offer','utility_data.IVT.coef', 'utility_data.IVT.offer','utility_data.MonetaryCost.coef', 'utility_data.MonetaryCost.offer','utility_data.TransferPenalty.coef','utility_data.TransferPenalty.offer', 'utility_data.WaitT.coef', 'utility_data.WaitT.offer', 'utility_data.WalkT.coef', 'utility_data.WalkT.offer', 'utility_data.utility'],axis=1)

#%%% Table 1 : Oprator Request  ,  Table 2 : Vehicle Comminantion. 
 

request_events=events[events['type']=='request']
vehicle_events=events[events['type']=='vehicle']


#%% Clean Tables

vehicle_events=vehicle_events.drop(['end_position.x', 'end_position.y','vehicle','segment', 'segment_mode','type'],axis=1)
vehicle_events=vehicle_events.reset_index(drop=True)
request_events=request_events.drop([ 'type','sim_id','used_capacity', 'path', 'path_length', 'request','segment', 'segment_mode'],axis=1)
request_events=request_events.reset_index(drop=True)


#%%% Table 1 : Trips to request  ,  Table 2 : Trips to drstantion. For Trips Anlysis 

vehicle_trips_to_req=vehicle_events[vehicle_events['state'].isin(['TravellingToOrigin'])]
vehicle_trips_to_dest=vehicle_events[vehicle_events['state'].isin(['TravellingToDestination'])]

#%%% Status  Vector
request_events.loc[request_events['state']=='START','Description']='AMOD Car start travel to the passenger location'
request_events.loc[request_events['state']=='SEGMENT_STARTED','Description']='AMOD Car that Pich up Passenger'
request_events.loc[request_events['state']=='SEGMENT_COMPLETED','Description']='AMOD Car finish trip'

stat=request_events.groupby('Description')['state'].count()
stat.loc['Total Number of Amod Cars']=len(vehicle_events.groupby('id')['state'].count())


#%%% Distance  Vector

vehicle_trips_to_dest_distruboutuin=vehicle_trips_to_dest.groupby('id')['state'].count().to_frame()
vehicle_trips_to_dest_distruboutuin=vehicle_trips_to_dest_distruboutuin.groupby('state')['state'].count().to_frame()
vehicle_trips_to_dest_distruboutuin=vehicle_trips_to_dest_distruboutuin.set_index(vehicle_trips_to_dest_distruboutuin.index.to_series().apply(lambda t: 'Total Number of Amod Cars make  %s trips' % (t)))

stat=stat.to_frame()
stat=pd.concat([stat,vehicle_trips_to_dest_distruboutuin], axis=0) 

stat.loc['Total Traveling Length (Km) of Amod Fleet']=(vehicle_trips_to_req['path_length'].sum()+vehicle_trips_to_dest['path_length'].sum())/1000
stat.loc['Total Traveling Length to Pasennger (Km)']=(vehicle_trips_to_req['path_length'].sum())/1000
stat.loc['Total Traveling Length to of trip destination (Km)']=(vehicle_trips_to_dest['path_length'].sum())/1000

stat.loc['Mean Traveling Length of Amod Fleet (Km)']=((vehicle_events[vehicle_events['state'].isin(['TravellingToOrigin','TravellingToDestination'])]['path_length'])/1000).mean()
stat.loc['Mean Traveling to Pasennger Length (Km)']=(vehicle_trips_to_req['path_length'].mean())/1000
stat.loc['Mean Traveling to of trip destination Length (Km)']=(vehicle_trips_to_dest['path_length'].mean())/1000


#%% Start Time Vector

vehicle_trips_to_dest=vehicle_trips_to_dest.copy()
vehicle_trips_to_dest['time_round'] = vehicle_trips_to_dest.time.apply(pd.to_datetime) 
vehicle_trips_to_dest['time_round']= pd.to_datetime(vehicle_trips_to_dest['time_round']).dt.floor('15T').dt.time
vehicle_trips_to_time_start_distruboutuin=vehicle_trips_to_dest.groupby('time_round')['state'].count().to_frame()
vehicle_trips_to_time_start_distruboutuin=vehicle_trips_to_time_start_distruboutuin.set_index(vehicle_trips_to_time_start_distruboutuin.index.to_series().apply(lambda t: 'Total Number of Amod Cars on interval  (top) that start trip  %s ' % (t)))
stat=pd.concat([stat,vehicle_trips_to_time_start_distruboutuin], axis=0) 

#%% Status  Vector 2

vehicle_events_travel_time_to_req=vehicle_events[vehicle_events['state'].isin(['TravellingToOrigin','PickupDone'])]
vehicle_events_travel_time_to_des=vehicle_events[vehicle_events['state'].isin(['TravellingToDestination','DeliveryDone'])]

vehicle_events_travel_time_to_des_finish_or_not=vehicle_events_travel_time_to_des['state'].value_counts()
stat.loc['Startet but Dont finished trips to destantion  ']=vehicle_events_travel_time_to_des_finish_or_not['TravellingToDestination']-vehicle_events_travel_time_to_des_finish_or_not['DeliveryDone']
vehicle_events_travel_time_to_des_finish_or_not=vehicle_events_travel_time_to_req['state'].value_counts()
stat.loc['Startet but Dont finished trips to passenger  ']=vehicle_events_travel_time_to_des_finish_or_not['TravellingToOrigin']-vehicle_events_travel_time_to_des_finish_or_not['PickupDone']
stat.loc['Startet Amod Trips to destantion']=len(vehicle_trips_to_dest)


#%% Travel  Time
  
request_events_summery=request_events[request_events['state'].isin(['SEGMENT_STARTED','SEGMENT_COMPLETED'])]
request_events_summery=request_events_summery.copy()
request_events_summery['time'] = request_events_summery.time.apply(pd.to_datetime) 
request_events_summery['time_2']=request_events_summery['time']
travel_times=request_events_summery.groupby('id').agg({'id':'count','time':'min','time_2':'max'})
travel_times=travel_times[travel_times['id']>1]
travel_times['delta']=travel_times['time_2']-travel_times['time']
travel_times['delta']=travel_times['delta'].apply(lambda x:x.total_seconds()/60)
travel_times['delta']=travel_times['delta'].apply('floor')

stat.loc['Mean trvel time to destenation ']=travel_times['delta'].mean()
travel_times['delta_grop']=(travel_times['delta']//10)*10

###merge to trips 
vehicle_trips_to_dest=vehicle_trips_to_dest.merge(travel_times,left_on='request',right_on=travel_times.index,how='left')
vehicle_trips_to_dest['delta_int']=vehicle_trips_to_dest['delta']
vehicle_trips_to_dest['delta']=vehicle_trips_to_dest['delta'].fillna('Dont finish!')

travel_times=travel_times.groupby('delta_grop')['id'].count().to_frame()
travel_times=travel_times.set_index(travel_times.index.to_series().apply(lambda t: 'Number of Amod Cars with travel time  (min)   %s ' % (t)))
travel_times=travel_times.rename({'id':'state'},axis=1)
stat=pd.concat([stat,travel_times], axis=0) 

#%% Make Some Table
stat=stat.copy()
vehicle_trips_to_dest=vehicle_trips_to_dest.copy()
vehicle_trips_to_req=vehicle_trips_to_req.copy()


transformer2 = Transformer.from_crs("EPSG:2039", "EPSG:4141")
request_events['position_1']=request_events.apply(lambda x: transformer2.transform(x['position.x'],x['position.y']),axis=1 )

request_events.to_csv(req)
vehicle_trips_to_dest.to_csv(trips_to_dest)
vehicle_trips_to_req.to_csv(trips_to_req)
stat.to_csv(stat1)
vehicle_events.to_csv(all_veh_events)






#%% Make Class for Json  


class Out:
    def __init__(self, list_of_cordinats,path_length,time,start_time,sim_id,idd,request):
        
        self.type = "Feature"
        self.properties = {'id':idd ,'path_length':path_length,'travel_time':time,'start_time':start_time,'sim_id':sim_id,'id':idd,'request':request}
        self.geometry={'type':'LineString',"coordinates":list_of_cordinats}
        
        
    def to_dict(self):    
        return {"type": self.type, "properties": {'id':self.properties['id'], 'path_length':self.properties['path_length'],'travel_time':self.properties['travel_time'],'start_time':self.properties['start_time'],'sim_id':self.properties['sim_id'],'request':self.properties['request']}, "geometry": {'type':self.geometry['type'],'coordinates':self.geometry['coordinates']}}
    
#%% GEO JSON from dest trips
transformer = Transformer.from_crs("EPSG:2039", "EPSG:4141")
vehicle_trips_to_dest['path']=vehicle_trips_to_dest['path'].apply(lambda x:[ [transformer.transform(a['x'],a['y'])[1],transformer.transform(a['x'],a['y'])[0]] for a in x] )
vehicle_trips_to_dest['geo_path']=vehicle_trips_to_dest['path'].apply(lambda x:[ list(a) for a in x] )

vehicle_trips_to_dest['out object']=vehicle_trips_to_dest.apply(lambda x:Out(x['geo_path'],x['path_length']/1000,x['delta_int'],x['time_x'],x['sim_id'],x['id_x'],x['request']), axis=1)

list_of_oupots=vehicle_trips_to_dest['out object'].to_list()
results = [obj.to_dict() for obj in list_of_oupots]

jsdata = json.dumps({"type": "FeatureCollection","features": results})
with open(geojson_dest, "w") as outfile:
    outfile.write(jsdata)


#%% GEO JSON from dest trips
transformer = Transformer.from_crs("EPSG:2039", "EPSG:4141")
vehicle_trips_to_req['path']=vehicle_trips_to_req['path'].apply(lambda x:[ [transformer.transform(a['x'],a['y'])[1],transformer.transform(a['x'],a['y'])[0]] for a in x] )
vehicle_trips_to_req['geo_path']=vehicle_trips_to_req['path'].apply(lambda x:[ list(a) for a in x] )
vehicle_trips_to_req['out object']=vehicle_trips_to_req.apply(lambda x:Out(x['geo_path'],x['path_length']/1000,0,x['time'],x['sim_id'],x['id'],x['request']), axis=1)


list_of_oupots=vehicle_trips_to_req['out object'].to_list()
results = [obj.to_dict() for obj in list_of_oupots]

jsdata = json.dumps({"type": "FeatureCollection","features": results})
with open(geojson_req, "w") as outfile:
    outfile.write(jsdata)

#%%

print(stat)















