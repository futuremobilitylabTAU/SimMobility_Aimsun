
<img src="[https://ik.imagekit.io/ikmedia/women-dress-2.jpg](https://imgbb.com/"><img src="https://i.ibb.co/hZLYjgc/2.png)" 
     width="150" 
     height="150" />
     
# simmobility aimsun 


*This repository houses extensive data facilitating the smooth integration between two simulators: SimMobility for preday demand simulation and Aimsun Next for supply (road network) simulation.**


<a href="https://ibb.co/vC5b8b9"><img src="https://i.ibb.co/mrsm7mp/Whats-App-Image-2023-11-15-at-09-52-21-eaf3dae6.jpg" alt="Whats-App-Image-2023-11-15-at-09-52-21-eaf3dae6" border="0"></a>


**1. The prime code from ubuntu terminal is (for iteration 1 to 40)  :**

------------------------------------------------------------START-------------------------------------------------------------------------------


for i in {1..40}; do cd  &&  

echo "iteration" $i  &&

cd "***/home/yedidya/simmobility/dev/Basic***" &&

***Release/SimMobility_Medium data/simulation2017_new_lua.xml data/simrun_MidTerm2017_new_lua.xml*** &&

mkdir -p ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/"$i"/Demand*** &&

mkdir -p ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/"$i"/Supply*** &&

mkdir -p ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/temp*** &&

cp ***/home/yedidya/simmobility/dev/Basic/activity_schedule /home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/"$i"/Demand/das_"$i"*** &&

python3 ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/Scripts/simo_outputs.py $i*** &&
python3 ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/Scripts/simo_taz_change.py $i*** &&

cp ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/model.ang*** && 

***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/"$i"/Supply/iteration_"$i".ang*** &&

cd &&

cd "***/home/yedidya/Aimsun_Next_22***" &&

./aconsole -v --log --log_file "***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/"$i"/Supply/log_iteraration_"$i""*** --project "***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/"$i"/Supply/iteration_"$i".ang***" --command execute --target 18393713 &&

cd &&

sudo -i -u postgres psql tel_aviv_1 -c "COPY **demand.learned_amcosts** TO '***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/temp/prev_learned_amcosts.csv***' CSV HEADER ESCAPE '''';" &&

cp ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/temp/prev_learned_amcosts.csv*** ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/"$i"/Demand/prev_learned_amcosts_"$i".csv*** &&

python3 ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/Scripts/aimso-outputs.py*** $i &&

cp ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/"$i"/Demand/am_from_sim_"$i".csv*** ***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/temp/learned_amcosts.csv*** &&

  sudo -i -u postgres psql **tel_aviv_1** -c " DELETE FROM **demand.learned_amcosts**" &&
  
  sudo -i -u postgres psql **tel_aviv_1** -c "COPY **demand.learned_amcosts** FROM '***/home/yedidya/Dropbox/Operating_Autonomous_Vehicles_in_Israel/Rebalance/Full_Rebalance/temp/learned_amcosts.csv***' DELIMITER ',' CSV HEADER ;" &&
  
  echo "done iteration -------------------------------------------------------------------------------------------------"; done

------------------------------------------------------------END-------------------------------------------------------------------------------

you need to make configuration of the folders and files, replications, and location and attach files in the scripts.
 
**2. The file "simo_taz_change" is not necessary if the AIMSUN centroid external id represents the DAS zones**

**3. "simo_outputs" makes analysis of Das after a preday run. (you need the individual table for this)**

**4. The file aimso_outputs make analysis from sqlite file + update am cost file + save linear regression  pict.**

**5. you need that in your expremient  on aimsun next make a "before-run" script that makes a matrix from das (script that i sent you) but in some changes so i send again + the external file. see that you need the code the position of iteration number on the aimsun file path**


**I recommend executing the code line by line, for example first:**

for i in {1..40}; do cd  &&  echo "iteration" $i  &&
  cd "/home/yedidya/simmobility/dev/Basic" &&
  echo "done iteration -------------------------------------------------------------------------------------------------"; done

**Then carefully add command by  command   according to the configuration of your run**
