
def filter(experiment):
    import pandas as pd
    import sys
    import PyQt5
    sys.path.append('/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/Aimsun_Script')
    import SortyByMode_12_12_22
    m=GKSystem.getSystem().getActiveModel().getDocumentFileName()
    try:
        i_prime=int(m[87:89])
        print(m[87:89])
    except:
        i_prime=int(m[87:88])
        print(m[87:89])
    start_time=0 ### 0=6.25 1=6.75 , 2=7.25...............
    end_time=10
    path=r'/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/%s'%(i_prime)
    path_file=path+'/Demand/das_taz_%s'%(i_prime)
    das=pd.read_csv(path_file,header='infer')
    centroid_id=pd.read_csv(r"/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/Aimsun_Script/Id.csv",header='infer')
    matrix_start_time=[QTime(6,0,0,0) ,QTime(6,30,0,0), QTime(7,0,0,0),QTime(7,30,0,0),QTime(8,0,0,0),QTime(8,30,0,0),QTime(9,0,0,0),QTime(9,30,0,0), QTime(10,0,0,0),QTime(10,30,0,0), QTime(11,0,0,0),QTime(11,30,0,0),QTime(12,0,0,0),QTime(12,30,0,0), QTime(13,0,0,0),QTime(13,30,0,0),  QTime(14,0,0,0),QTime(14,30,0,0),QTime(15,0,0,0),QTime(15,30,0,0), QTime(16,0,0,0),QTime(16,30,0,0),QTime(17,0,0,0),QTime(17,30,0,0),QTime(18,0,0,0),QTime(18,30,0,0), QTime(19,0,0,0),QTime(19,30,0,0), QTime(20,0,0,0),QTime(20,30,0,0), QTime(21,0,0,0),QTime(21,30,0,0), QTime(22,0,0,0),QTime(22,30,0,0),QTime(23,0,0,0),QTime(23,30,0,0), QTime(0,0,0,0),QTime(0,30,0,0), QTime(1,0,0,0),QTime(1,30,0,0), QTime(2,0,0,0),QTime(2,30,0,0), QTime(3,0,0,0),QTime(3,30,0,0),QTime(4,0,0,0),QTime(4,30,0,0), QTime(5,0,0,0),QTime(5,30,0,0)]
    mode_loop=['Car']
    for j10 in mode_loop:
        mode=j10
        matrix_name_strings=['matrix_6.25_%s'%mode, 'matrix_6.75_%s'%mode, 'matrix_7.25_%s'%mode,'matrix_7.75_%s'%mode,'matrix_8.25_%s'%mode, 'matrix_8.75_%s'%mode,'matrix_9.25_%s'%mode, 'matrix_9.75_%s'%mode, 'matrix_10.25_%s'%mode,'matrix_10.75_%s'%mode, 'matrix_11.25_%s'%mode, 'matrix_11.75_%s'%mode,'matrix_12.25_%s'%mode, 'matrix_12.75_%s'%mode,  'matrix_13.25_%s'%mode, 'matrix_13.75_%s'%mode,  'matrix_14.25_%s'%mode, 'matrix_14.75_%s'%mode,'matrix_15.25_%s'%mode, 'matrix_15.75_%s'%mode, 'matrix_16.25_%s'%mode, 'matrix_16.75_%s'%mode,'matrix_17.25_%s'%mode, 'matrix_17.75_%s'%mode, 'matrix_18.25_%s'%mode,  'matrix_18.75_%s'%mode, 'matrix_19.25_%s'%mode, 'matrix_19.75_%s'%mode,  'matrix_20.25_%s'%mode,  'matrix_20.75_%s'%mode, 'matrix_21.25_%s'%mode,  'matrix_21.75_%s'%mode,  'matrix_22.25_%s'%mode, 'matrix_22.75_%s'%mode, 'matrix_23.25_%s'%mode, 'matrix_23.75_%s'%mode,  'matrix_24.25_%s'%mode,  'matrix_24.75_%s'%mode, 'matrix_25.25_%s'%mode,  'matrix_25.75_%s'%mode,  'matrix_26.25_%s'%mode,  'matrix_26.75_%s'%mode, 'matrix_3.25_%s'%mode,  'matrix_3.75_%s'%mode,  'matrix_4.25_%s'%mode, 'matrix_4.75_%s'%mode, 'matrix_5.25_%s'%mode, 'matrix_5.75_%s'%mode]
        for t in range(start_time,end_time)  :
            flag=False
            matrix=SortyByMode_12_12_22.fo(das,mode,t,centroid_id) ## Builed trips matrix in external founctuin by mode and time
            gabii=matrix.values.tolist() ### make list from this dataframe
            c=model.getType("GKCentroidConfiguration")  
            d=GK.GetObjectsOfType(c) #### d is list of all CentroidConfiguration
            for j in d:
                if(j.isActive()==True) :
                    print("this one is active!") 
                    list_of_objects_that_matrix=j.getODMatrices()  ## Return a "GKfolder" thats is a list of objects
                    for j1 in list_of_objects_that_matrix:    ## for each object in the llist    
                        if(j1.getName()==matrix_name_strings[t]): #### upste matrix only if the name of the matrix merge the name in matrix_name list by correct time
                            flag=True
                            j1.setTripsFromList(gabii) ### update matrix by the list
                            print(j1.getName())   ##print matrix name
                            print(j1.getTotalTrips())   ##print total trips in the matrix
                            t_2=matrix_start_time[t]            ##this update starte time of matrix from the list of starts time    ,    t_2=PyQt5.QtCore.QTime.currentTime ()
                            j1.setDataValue(model.getColumn( "GKTrafficDemandItem::fromAtt"),t_2) ## to ubdate the time we need get the Coulome of start time ,thiis colum + out time is the atrgument to set time in (GK object)ODMATRIX
                            print("matrix new start time:")
                            print(j1.getDataValueTime(model.getColumn( "GKTrafficDemandItem::fromAtt"))) ###print the time.
                            j1.setDataValue(model.getColumn( "GKTrafficDemandItem::durationAtt"),QTime(0,30,0,0)) ## ubdate interval time of metrix to 30 min 
                            vvt_list=GK.GetObjectsOfType(model.getType("GKVehicle"))  ##  the vechule type list
                            for vvt in vvt_list :
                                   if (vvt.getName()==mode):
                                       j1.setVehicle(vvt) ### put the vecyle type to the ODMATRIX
                                       break
                          
                            break
                    if(flag==False): 
                        cmd = model.createNewCmd( model.getType( "GKODMatrix" )) ##Builed object type ODMATRIX 
                        cmd.setCentroidConfiguration(j)  ## Set is Centroied Configure be thats one is active
                        model.getCommander().addCommand(cmd) ## comment the model
                        res = cmd.createdObject()
                        res.setName(matrix_name_strings[t])
                        res.setDataValue(model.getColumn( "GKTrafficDemandItem::durationAtt"),QTime(0,30,0,0)) ## ubdate interval time of metrix to 30 min
                        res.setDataValue(model.getColumn( "GKTrafficDemandItem::fromAtt"),matrix_start_time[t])
                        res.setTripsFromList(gabii)
                        print(res.getName())   ##print matrix name
                        print(res.getTotalTrips())   ##print total trips in the matrix
                        print("matrix new start time:")
                        print(res.getDataValueTime(model.getColumn( "GKTrafficDemandItem::fromAtt"))) ###print the time.
                        vvt_list=GK.GetObjectsOfType(model.getType("GKVehicle"))  ##  the vechule type list
                        for vvt in vvt_list :   
                            if(mode==vvt.getName()):
                                res.setVehicle(vvt)

    return True


