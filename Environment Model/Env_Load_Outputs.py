import pandas as pd
import sys
import numpy as np
import ast
### impot ptyhon folder and file 
sys.path.append('/home/yedidya/Dropbox/Working_Model_Aimsun_TLV/Paper_env/Script_confing')
result_folder=r'/home/yedidya/Dropbox/Aimsun -Cellular Assigment/Aimsun Model'

 

section_type=model.getType("GKSection")
co_2 = section_type.addColumn( "GKSection::hot_co2", "Hot_CO2_Israel", GKColumn._GKTimeSerie) #### make new field to co2 hot emmision
nox = section_type.addColumn( "GKSection::hot_nox", "Hot_NOX_Israel", GKColumn._GKTimeSerie) #### make new field to NOX hot emmision
pm = section_type.addColumn( "GKSection::hot_pm", "Hot_PM2.5_Israel", GKColumn._GKTimeSerie) #### make new field to PM hot emmision
voc = section_type.addColumn( "GKSection::hot_voc", "Hot_VOC_Israel", GKColumn._GKTimeSerie) #### make new field to VOC hot emmision
fc = section_type.addColumn( "GKSection::fc", "fc_Israel", GKColumn._GKTimeSerie) #### make new field to VOC hot emmision
tp=19

section_table = pd.read_csv(result_folder+'/section_table.csv')
### run over model sections

for ind in section_table.index:
         print(section_table['Section-ID'][ind])
         id=section_table['Section-ID'][ind]
         id_int=id.item()
         road=model.getCatalog().find(id_int)
         Length=road.getDataValueDouble(model.getColumn("GKPolyline::length3DAttr"))/1000


         co2_israel=model.getColumn("GKSection::hot_co2")
         fc_israel=model.getColumn("GKSection::fc")
         nox_israel=model.getColumn("GKSection::hot_nox")
         pm_israel=model.getColumn("GKSection::hot_pm")
         voc_israel=model.getColumn("GKSection::hot_voc")

         TS_Count=road.getDataValueTS(model.getColumn("DYNAMIC::SRC_GKSection_count_0")) ## return time series type of density
         d=TS_Count.getDescription()
 
         co_list=ast.literal_eval(section_table['Co2'][ind])
         nox_list=ast.literal_eval(section_table['Nox'][ind])
         nmvoc_list=ast.literal_eval(section_table['NMVOC'][ind])
         pm_list=ast.literal_eval(section_table['PM2.5'][ind])
         fc_list=ast.literal_eval(section_table['FC'][ind])



         for i in range(tp):   
                  t=GKTimeSerieIndex (i)
                  road.setDataValueInTS(co2_israel,t,co_list[i]/Length,0,0,d)    
                  road.setDataValueInTS(nox_israel,t,nox_list[i]/Length,0,0,d)               
                  road.setDataValueInTS(fc_israel,t,fc_list[i]/Length,0,0,d)               
                  road.setDataValueInTS(voc_israel,t,nmvoc_list[i],0,0,d)   
                  road.setDataValueInTS(pm_israel,t,pm_list[i],0,0,d)               
            
           


print('end-loading')








