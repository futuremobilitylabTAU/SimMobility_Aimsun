import pandas as pd
import sys

### impot ptyhon folder and file 
sys.path.append('/home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing')
result_folder=r'/home/yedidya/Dropbox/Aimsun -Cellular Assigment/Aimsun Model'

import Founction_car_linux


section_type=model.getType("GKSection")
co_2 = section_type.addColumn( "GKSection::hot_co2", "Hot_CO2_Israel", GKColumn._GKTimeSerie) #### make new field to co2 hot emmision
nox = section_type.addColumn( "GKSection::hot_nox", "Hot_NOX_Israel", GKColumn._GKTimeSerie) #### make new field to NOX hot emmision
pm = section_type.addColumn( "GKSection::hot_pm", "Hot_PM2.5_Israel", GKColumn._GKTimeSerie) #### make new field to PM hot emmision
voc = section_type.addColumn( "GKSection::hot_voc", "Hot_VOC_Israel", GKColumn._GKTimeSerie) #### make new field to VOC hot emmision
fc = section_type.addColumn( "GKSection::fc", "fc_Israel", GKColumn._GKTimeSerie) #### make new field to VOC hot emmision
tp=19

section_table = pd.DataFrame(columns=['Section-ID','Limit-Speed','Road-Type','Length','Density','Flow','Speed','Co2','Nox','NMVOC','PM2.5','FC'])
### run over model sections
road_list=GK.GetObjectsOfType(section_type)
j=0
for road in road_list:
               print("ID:")
               id=road.getDataValueInt(model.getColumn("GKObject::idAtt"))
               print(id)
               print("Limit Speed:")
               print(road.getDataValueDouble(model.getColumn("GKSection::speedAtt")))
               print("Road Type:")
               print(road.getDataValueObject(model.getColumn("GKSection::roadTypeAtt")).getName())
               Road_type=road.getDataValueObject(model.getColumn("GKSection::roadTypeAtt")).getName()
               Speed_Limit=road.getDataValueDouble(model.getColumn("GKSection::speedAtt"))
               Length=road.getDataValueDouble(model.getColumn("GKPolyline::length3DAttr"))/1000
               print(Length)

                 
#################################### Make Density List from EXP result in each road.
               print("Denssity road:")
               TS_Density=road.getDataValueTS(model.getColumn("DYNAMIC::SRC_GKSection_density_0")) ## return time series type of density
               TS_Density_List=[]
               for i in range(tp): 
                     t=GKTimeSerieIndex (i)
                     TS_Density_List.append(TS_Density.getValue(t))
               print(TS_Density_List)


#################################### Make Flow List from EXP result in each road.
               print("Flow road:")
               TS_Flow=road.getDataValueTS(model.getColumn("DYNAMIC::SRC_GKSection_flow_0")) ## return time series type of density
               TS_Flow_List=[]
               for i in range(tp): 
                     t=GKTimeSerieIndex (i)
                     TS_Flow_List.append(TS_Flow.getValue(t))
               print(TS_Flow_List)


#################################### Make Density List from EXP result in each road.
               print("Speed road:")
               TS_Speed=road.getDataValueTS(model.getColumn("DYNAMIC::SRC_GKSection_speed_0")) ## return time series type of density
               TS_Speed_List=[]
               for i in range(tp): 
                     t=GKTimeSerieIndex (i)
                     TS_Speed_List.append(TS_Speed.getValue(t))
               print(TS_Speed_List)

#################################### Make Count List from EXP result in each road.
               print("Count road:")
               TS_Count=road.getDataValueTS(model.getColumn("DYNAMIC::SRC_GKSection_count_0")) ## return time series type of density
               TS_Count_List=[]
               for i in range(tp): 
                     t=GKTimeSerieIndex (i)
                     TS_Count_List.append(TS_Count.getValue(t))
               print(TS_Count_List)


#########################################################
               print("Co2 Emmosion:")
               pelet=Founction_car_linux.make_co2_by_tables(TS_Density_List,TS_Count_List,TS_Speed_List,Speed_Limit,Road_type,Length)
               print(pelet)
               co2_israel=model.getColumn("GKSection::hot_co2")
               d=TS_Count.getDescription()
               for i in range(tp): 
                     t=GKTimeSerieIndex (i)      
                     road.setDataValueInTS(co2_israel,t,pelet[i]/Length,0,0,d)

 ###################                  
               print("FC:")
               pelet5=Founction_car_linux.make_fc_by_tables(TS_Density_List,TS_Count_List,TS_Speed_List,Speed_Limit,Road_type,Length)
               print(pelet5)
               fc_israel=model.getColumn("GKSection::fc")
               d=TS_Count.getDescription()
               for i in range(tp): 
                     t=GKTimeSerieIndex (i)
                     road.setDataValueInTS(fc_israel,t,pelet5[i]/Length,0,0,d)


    ###################                  
               print("Nox Emmosion:")
               pelet2=Founction_car_linux.make_nox_by_tables(TS_Density_List,TS_Count_List,TS_Speed_List,Speed_Limit,Road_type,Length)
               print(pelet2)
               nox_israel=model.getColumn("GKSection::hot_nox")
               d=TS_Count.getDescription()
               for i in range(tp): 
                     t=GKTimeSerieIndex (i)
                     road.setDataValueInTS(nox_israel,t,pelet2[i]/Length,0,0,d)

    ###################                  
               print("PM2.5 Emmosion:")
               pelet3=Founction_car_linux.make_pm_by_tables(TS_Density_List,TS_Count_List,TS_Speed_List,Speed_Limit,Road_type,Length)
               print(pelet3)
               pm_israel=model.getColumn("GKSection::hot_pm")
               d=TS_Count.getDescription()
               for i in range(tp): 
                     t=GKTimeSerieIndex (i)
                     road.setDataValueInTS(pm_israel,t,pelet3[i],0,0,d)

    ###################                  
               print("VOC Emmosion:")
               pelet4=Founction_car_linux.make_voc_by_tables(TS_Density_List,TS_Count_List,TS_Speed_List,Speed_Limit,Road_type,Length)
               print(pelet4)
               voc_israel=model.getColumn("GKSection::hot_voc")
               d=TS_Count.getDescription()
               for i in range(tp): 
                     t=GKTimeSerieIndex (i)
                     road.setDataValueInTS(voc_israel,t,pelet4[i],0,0,d)

               add={'Section-ID':id, 'Limit-Speed':Speed_Limit, 'Road-Type':Road_type, 'Length':Length,'Density':TS_Density_List  ,'Flow':TS_Flow_List,'Speed':TS_Speed_List,'Co2':pelet,'Nox':pelet2,'NMVOC':pelet4,'PM2.5':pelet3,'FC':pelet5} 
               section_table.loc[j]=add
               j=j+1


section_table.to_csv(result_folder+'/section_table.csv')
