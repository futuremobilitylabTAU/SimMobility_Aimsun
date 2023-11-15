import pandas as pd
import numpy as np


print("Enter to Ex-File")


def fo(das,mode,t,transformation_list):

    print('"len das"')
    print(len(das))
    das=das[das['prev_stop_zone'].isin([41,42,43])==False]
    das=das[das['stop_zone'].isin([41,42,43])==False]
    print('"len das witout 41 42 43"')
    print(len(das))
    print('"Enter to Ex-Founction"')
    das=das.merge(transformation_list,left_on='prev_stop_zone' ,right_on='Ex',how='left')
    das['prev_stop_zone_new']= das['Aimsun']
    das=das.merge(transformation_list,left_on='stop_zone' ,right_on='Ex',how='left')
    das['stop_zone_new']= das['Aimsun_y']
    print("Update the ID")
    das["prev_stop_departure_time"] = pd.to_numeric(das["prev_stop_departure_time"])
    arry=np.array([6.25, 6.75, 7.25,7.75, 8.25, 8.75,9.25, 9.75, 10.25,10.75, 11.25, 11.75,12.25, 12.75, 13.25,13.75, 14.25, 14.75,15.25, 15.75, 16.25, 16.75,17.25, 17.75, 18.25, 18.75,19.25, 19.75, 20.25, 20.75,21.25, 21.75, 22.25,22.75,23.25, 23.75, 24.25, 24.75,25.25, 25.75, 26.25, 26.75,3.25, 3.75, 4.25,4.75,5.25,5.75])
    das_filter=das[das['prev_stop_departure_time']==arry[t]]
    das_filter=das_filter[das_filter['stop_mode']==mode]
    das_filter=das_filter[das_filter['prev_stop_zone_new']!=das_filter['stop_zone_new']]
    matrix=das_filter.groupby(['prev_stop_zone_new','stop_zone_new']).count()
    matrix=matrix['model']
    matrix = matrix.unstack(level=0)
    matrix=matrix.fillna(0)
    matrix=matrix.T
    print("Done make grupe by")

    
    matrix_empty=pd.DataFrame(columns=transformation_list['Aimsun'],index=transformation_list['Aimsun'])
    matrix_empty=matrix_empty.fillna(0)
    matrix  = matrix.combine_first(matrix_empty)
    
    print('"EXIT the Ex-Founction"')


    

    return matrix
    



  
### Test

#das=pd.read_csv("activity_schedule",header=None)
#das.columns = ['person_id', 'tour_no', 'tour_type', 'stop_no', 'stop_type', 'stop_location', 'stop_zone','stop_mode', 'primary_stop', 'arrival_time', 'departure_time', 'prev_stop_location', 'prev_stop_zone', 'prev_stop_departure_time', 'drivetrain', 'make', 'model']
#centroid=pd.read_csv("id.csv",header='infer')
#a='Car'
#b=4
#out=fo(das,a,b,centroid)

