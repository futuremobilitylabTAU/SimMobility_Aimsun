#%%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys
i_prime=sys.argv[1]
print(i_prime)

result_folder=r'/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/%s'%i_prime
result_folder_file=result_folder+'/Demand/das_%s'%i_prime

path_das=result_folder_file
das = pd.read_csv(path_das, header=None, names=['person_id', 'tour_no', 'tour_type', 'stop_no', 'stop_type', 'stop_location', 'stop_zone', 'stop_mode', 'primary_stop', 'arrival_time', 'departure_time', 'prev_stop_location',  'prev_stop_zone', 'prev_stop_departure_time', 'drivetrain', 'make', 'model'])

key=r'/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/Scripts/key.csv'
key = pd.read_csv(key)


das=das.merge(key,left_on='stop_zone',right_on='zone_id',how='left')
das=das.drop(['stop_zone','zone_id'],axis=1)
das=das.rename({'zone_code':'stop_zone'},axis=1)

das=das.merge(key,left_on='prev_stop_zone',right_on='zone_id',how='left')
das=das.drop(['prev_stop_zone','zone_id'],axis=1)
das=das.rename({'zone_code':'prev_stop_zone'},axis=1)

das=das.merge(key,left_on='stop_location',right_on='zone_id',how='left')
das=das.drop(['stop_location','zone_id'],axis=1)
das=das.rename({'zone_code':'stop_location'},axis=1)

das=das.merge(key,left_on='prev_stop_location',right_on='zone_id',how='left')
das=das.drop(['prev_stop_location','zone_id'],axis=1)
das=das.rename({'zone_code':'prev_stop_location'},axis=1)


result_folder=r'/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/%s/Demand'%i_prime
result_folder_file=result_folder+'/das_taz_%s'%i_prime
das.to_csv(result_folder_file)
