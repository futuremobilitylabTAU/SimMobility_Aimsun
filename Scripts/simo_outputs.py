
import pandas as pd
import numpy as np
import sys
pd.set_option('display.max_columns', None)
i_prime=sys.argv[1]
print(i_prime)

result_folder=r'/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/%s'%i_prime
result_folder_file=result_folder+'/Demand/das_%s'%i_prime





das=pd.read_csv( result_folder_file,header='infer', names=['person_id', 'tour_no', 'tour_type', 'stop_no', 'stop_type', 'stop_location', 'stop_zone', 'stop_mode', 'primary_stop', 'arrival_time', 'departure_time', 'prev_stop_location',  'prev_stop_zone', 'prev_stop_departure_time', 'drivetrain', 'make', 'model'])
fields = ['id','activity_address_id','fixed_workplace','work_at_home', 'home_address_id']
ind = pd.read_csv(r"/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/Scripts/table_individual_by_id_for_preday_25.csv",  usecols=fields)



das = das.sort_values(by = ['person_id','tour_no'],ascending =True)

#import the individual table to separate the fixed work location
#fields = ['individual_id','work_sla','fixed_work_location']

#3468004
#pop = 2606753
#pop = 1000000
#pop = 3784739


#################################################################################################
pop = 3468004
total_pop = 3468004
popratio = round(total_pop/pop)
#################################################################################################



#printing the total number of stops
print("-----------------DPB---------------------")
stopsNum = len(das.person_id)*popratio
print("Total number of activities: "+ str(stopsNum)+ "\n")
res =  pd.Series({'TotalStops':stopsNum})

#match the person_id to individual_id in both tables
das.person_id = das.person_id.str.replace(r'\D+', '').astype('int')
das.person_id = (das.person_id/10).astype(int)

dasTours = das[das['primary_stop']==True]

#printing total number of tours
print("-----------------DPT------------------------")
ToursNum =  len(dasTours.primary_stop)*popratio
print("Total number of tours: "+ str(ToursNum)+ "\n")
ToursType = dasTours.groupby("tour_type")['person_id'].count()
TourTypeProp = ((ToursType/ToursNum).round(4))
print((TourTypeProp*100).round(2).astype(str) + "%")
print()
res = res.append(TourTypeProp)

print("-----------------DPS-----------------------")
StopsType = das[das['stop_type']!='Home'].groupby("stop_type")['person_id'].count()
stopTypeProp = ((StopsType/(das['stop_type']!='Home').sum()).round(4))
print((stopTypeProp*100).round(2).astype(str) + "%")
print()
res = res.append(stopTypeProp)

print("----------------NTx------------------------")
print(ToursType*popratio )
print()
res=res.append(ToursType*popratio)

#separating between tours to work location and not-work location
dasW = das[(das['tour_type']=='Work')&(das['primary_stop']==True)]
#dasW = dasW.merge(ind,left_on ='person_id',right_on= 'individual_id',how = 'left')
dasW = dasW.merge(ind,left_on ='person_id',right_on= 'id',how = 'left')

#dasW['tf'] = np.where((dasW['stop_location']==dasW['work_sla']),'WorkPlace','NotWorkPlace')
dasW['tf'] = np.where((dasW['stop_location']==dasW['activity_address_id']),'WorkPlace','NotWorkPlace')
dasW['tf'] = np.where((dasW['work_at_home']) & (dasW['stop_location'] == dasW['home_address_id']), 'WorkPlace', dasW['tf'])

WorkPlaceTours = (dasW['tf']=='WorkPlace').sum()
UWratio = WorkPlaceTours/len(dasW)
print("----------------UW-----------------------------")
print('Usual wrok place ratio: ' + (UWratio*100).round(1).astype(str) +"%\n")
res = res.append(pd.Series({'UW':UWratio}))

dasTours = dasTours.merge(dasW[['person_id','tour_no','tf']],on=['person_id','tour_no'], how='left')

dasTours['NewType'] = dasTours['tour_type']
dasTours.loc[dasTours['tf'].notna(),'NewType'] = dasTours.loc[dasTours['tf'].notna(),'tf']

WorkTours = (dasTours['tour_type']=='Work').sum()

# printing modes by tour type
print("---------------TMx---------------------")
d = dasTours.groupby(['NewType','stop_mode']).size()
print (d * popratio)
print()

res = res.append((d * popratio).reset_index().iloc[:,2])


# intermediate stops
print("---------------isg-------------------")

a=das.groupby(['person_id','tour_no','primary_stop'])['stop_no'].max()
a=a.reset_index()
b=a[a['primary_stop']==True]
das = das.merge(b, on=['person_id','tour_no'],how='left')
das.rename({'stop_no_x':'stop_no','stop_no_y':'primery_no','primary_stop_x':'primary_stop'},axis=1,inplace=True)
das['inbound'] = np.where((das['stop_no'] < das['primery_no']), True, False)

dasStops = das[(das['primary_stop']==False) & (das['stop_type']!='Home')]
isg = dasStops.groupby('stop_type')
print(isg.size()*popratio)

res = res.append(((isg.size())*popratio).reset_index().iloc[:,1])

isg_in = dasStops.groupby(['inbound','stop_type'])
print((isg_in.size())*popratio)

res = res.append((isg_in.size()*popratio).reset_index().iloc[:,2])

print("---------------imd-------------------")
imd = dasStops.groupby('stop_mode')
print(imd.size()*popratio)

res = res.append(((imd.size())*popratio).reset_index().iloc[:,1])


# activities by mode
byMode = pd.DataFrame(das.groupby('stop_mode')['stop_mode'].count())
byMode['share'] = (byMode['stop_mode'] / (byMode['stop_mode'].sum()) *100).round(2)
print(byMode)

result_folder=r'/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/%s/Demand'%i_prime
byMode.to_csv(result_folder+'/byMode.csv')
(imd.size()*popratio).to_frame().to_csv(result_folder+'/imd.csv')
(d * popratio).to_frame().to_csv(result_folder+'/TMx.csv')
(ToursType*popratio).to_csv(result_folder+'/NTx.csv')
(TourTypeProp).to_frame().to_csv(result_folder+'/DPT.csv')
(stopTypeProp).to_frame().to_csv(result_folder+'/DPS.csv')


result_folder=r'/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/%s/Supply'%i_prime
for_aimsun=pd.DataFrame(data={'iteration':[i_prime]})
for_aimsun.to_csv(result_folder+'/for_aimsun')











for_aimsun.to_csv(result_folder+'/for_aimsun.csv')


