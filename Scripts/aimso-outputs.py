import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import math
import ast
import sys



i_prime=sys.argv[1]
print(i_prime)


key=r"/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/Scripts/id.csv"

result_folder=r'/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/%s'%i_prime
path_database=result_folder+'/Supply/iteration_%s.sqlite'%i_prime


path_am=result_folder+'/Demand/prev_learned_amcosts_%s.csv'%(i_prime)


path_new_am=result_folder+'/Demand/am_from_sim_%s.csv'%i_prime
###path_database

print(path_database)
#%%% Connect to Data Base Result Of Aimsun Next
con = sqlite3.connect(path_database)

trajectory = pd.read_sql_query("SELECT * from MEVEHTRAJECTORY", con)

con.close()
##############print(trajectory)


#%%% trajectory order and time cancoulation

trajectory=trajectory[['origin', 'destination','sid','exitTime','generationTime','speed','travelledDistance']]
trajectory['time']=trajectory['exitTime']-trajectory['generationTime']

#%%% only cars that trvael in the simulation time

trajectory=trajectory[trajectory['travelledDistance']>0]

#%% make mean in each  origin>destination
sumery=trajectory.groupby(['origin', 'destination'])[['time','speed','travelledDistance']].mean()
sumery['time']=sumery['time']/60
sumery['time']=sumery['time']/60
sumery=sumery.reset_index()
#%% the old am

am=pd.read_csv(path_am)
#%% key from aimsun to simo of zones
print(len(am))
key=pd.read_csv(key)

#%% make merge og the key in origin and destenation level

sumery=sumery.merge(key,left_on='origin',right_on='Aimsun',how='left')
sumery=sumery.rename({'Aimsun':'Aimsun-origin','Ex' :'Ex-origin','Sim':'origin_zone'},axis=1)
sumery=sumery.merge(key,left_on='destination',right_on='Aimsun',how='left')
sumery=sumery.rename({'Aimsun':'Aimsun-destination','Ex' :'Ex-destination','Sim':'destination_zone'},axis=1)

#%% merge to am the simulation data

sumery_to_merge=sumery[['origin_zone','destination_zone','time']]
am=am.merge(sumery_to_merge,on=['origin_zone','destination_zone'],how='left')

#%% if time dont updaeted , take the old time

am.loc[am['time'].isna()==True,'time']=am['car_ivt']

#%% Anysis of The Update (All Data)

fig4, axe4 = plt.subplots(nrows=1, ncols=1,figsize=(11,11))



X1 = am.iloc[:, 4].values.reshape(-1, 1)  
Y1 = am.iloc[:, 17].values.reshape(-1, 1) 
linear_regressor1 = LinearRegression()  
linear_regressor1.fit(X1, Y1)  
Y1_pred = linear_regressor1.predict(X1)  

##Plot
axe4.scatter(X1, Y1, color='#EC6B56')
axe4.plot(X1, Y1_pred, color='#47B39C')
axe4.set_title(' ' ,fontsize=25)
axe4.set_xlabel('Iteration 9 car ivt' , fontsize=25,labelpad=15)
axe4.set_ylabel('Iteration 10 car ivt', fontsize=25,labelpad=15)
axe4.set_xlim(0, 2)
axe4.set_ylim(0, 2)
axe4.text(0.7, 1.5, 'R-squared = %0.2f' % r2_score(Y1, Y1_pred),size=17)
axe4.text(0.7, 1.75, 'Coefficients = %0.2f' % linear_regressor1.coef_,size=17)
axe4.tick_params(axis='x', rotation=0,labelsize=18)
axe4.tick_params(axis='y', rotation=0,labelsize=18)
axe4.grid(color='#FFC154', linestyle='--', linewidth=0.3)

fig4.savefig(result_folder+'/Supply/regresion.png',dpi=500)

#%% learn about delta to anlysis

am['delta']=am['time']-am['car_ivt']



mean=am['delta'].mean()
res_old=pd.DataFrame(data={'mean time delta all':[mean]})
res_old.to_csv(result_folder+'/Supply/all_data_time_mean.csv')





#%% Only New Data 

am_only_new=am[am['delta']!=0]


mean=am_only_new['delta'].mean()
res_old=pd.DataFrame(data={'mean time delta new':[mean]})
res_old.to_csv(result_folder+'/Supply/new_data_time_mean.csv')


#%%% Final Update and save

am['car_ivt']=am['time']
am=am.drop(['time', 'delta'],axis=1)
am.to_csv(path_new_am,index=False)
print(len(am))

#%% Make Some Stats
trajectory=trajectory[trajectory['sid']==154]
trajectory['time']=trajectory['time']/60
trajectory['time']=trajectory['time']/60
trajectory['travelledDistance']=trajectory['travelledDistance']/1000
trajectory['speed_km_h']=trajectory['travelledDistance']/trajectory['time']

#%%

mean_speed=trajectory['speed_km_h'].mean()
mean_sidt=trajectory['travelledDistance'].mean()


res_newdata=pd.DataFrame(data={'mean speed':[mean_speed],'mean_distance':[mean_sidt]})
res_newdata.to_csv(result_folder+'/Supply/new_data_mean.csv')












