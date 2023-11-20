--[[
Model - Mode/destination choice for work tour to unusual location
Type - logit
Based on tmdw by Siyu Li, Harish Loganathan
Created by Isabel Viegas on February 22, 2017
]]

-- all require statements do not work with C++. They need to be commented. The order in which lua files are loaded must be explicitly controlled in C++. 
--require "Logit"

--Estimated values for all betas
--Note: the betas that not estimated are fixed to zero.

--!! see the documentation on the definition of AM,PM and OP table!!


local beta_cons_walk = 3.3 +0.2 -0.1 
local beta_cons_bike = -2.1   +0.1  +0.5 +0.1 +0.1
local beta_cons_drive1 = 4.95 -0.3 -0.2  -0.1 -0.1  -0.3 +0.1  +0.2  +1 -0.5 -0.1  +0.06 -0.05
local beta_cons_share2 = -0.7 +0.3 +0.1              
local beta_cons_share3 = 0.7   +0.1 +0.1         
local beta_cons_PB = 0                         
local beta_cons_PT = 1.64   -0.1             
local beta_cons_motor = 1.5  -1 +0.1 +0.1 +0.1  +0.2  +0.2  +0.2 
local beta_cons_taxi = 0  
local beta_cons_SMS = 0                            
local beta_cons_MRT = 1.64   -0.1             
--local beta_cons_AMOD = beta_cons_taxi
--local beta_cons_AMOD_Pool = beta_cons_taxi+beta_cost*1.197

local beta_cost = -0.253


local beta_tt_walk = -0.116
local beta_tt_bike = -0.184
local beta_tt_drive1 = -0.0452
local beta_tt_share2 = -0.0489
local beta_tt_share3 = -0.0915
local beta_tt_PT = -0.0527
local beta_tt_motor = -0.122
local beta_tt_taxi = -0.0452
local beta_tt_SMS = -0.0452
local beta_tt_MRT = -0.0527
--local beta_tt_AMOD = beta_tt_taxi
--local beta_tt_AMOD_Pool = beta_tt_taxi

beta_tt_walk = beta_tt_walk*60
beta_tt_bike =beta_tt_bike *60
beta_tt_drive1 =beta_tt_drive1*60
beta_tt_share2 =beta_tt_share2 *60
beta_tt_share3 = beta_tt_share3*60
beta_tt_PT = beta_tt_PT*60
beta_tt_motor =beta_tt_motor*60
beta_tt_taxi = beta_tt_taxi*60
beta_tt_SMS = beta_tt_SMS*60
beta_tt_MRT = beta_tt_MRT*60
--beta_tt_AMOD =beta_tt_AMOD *60
--beta_tt_AMOD_Pool = beta_tt_AMOD_Pool*60

local beta_employment = 7.37
local beta_log = 0.496
local beta_population = -29.2

local beta_cbd_notdrive = 0.428   +2  -1
local beta_cbd_drive1 = -1.72     +2  
local beta_cbd_share2 = -0.835    +2  
local beta_cbd_share3 = -1.36     +2  
local beta_cbd_PT = 0.947         +2 -1 -1
local beta_cbd_motor = (beta_cbd_PT + beta_cbd_notdrive)/2
local beta_cbd_taxi = (beta_cbd_PT + beta_cbd_notdrive)/2
local beta_cbd_SMS = (beta_cbd_PT + beta_cbd_notdrive)/2
local beta_cbd_rail_SMS = (beta_cbd_PT + beta_cbd_notdrive)/2
local beta_cbd_MRT = 0.947         +2 -1 -1
--local beta_cbd_AMOD= (beta_cbd_PT + beta_cbd_notdrive)/2
--local beta_cbd_AMOD_Pool = (beta_cbd_PT + beta_cbd_notdrive)/2

--choice set

local choice = {}

for i = 1, 917*11 do
	choice[i] = i
end

--utility

-- 1 for public bus; 2 for private bus; 3 for drive1;

-- 4 for shared2; 5 for shared3+; 6 for motor; 7 for walk; 8 for AMOD

-- 9 for AMOD_Pool, 10 for rail_SMS

local utility = {}

local function computeUtilities(params,dbparams)

	local female_dummy = params.female_dummy


	local cost_bus = {}
	local cost_private_bus = {}
	local cost_drive1 = {}
	local cost_share2 = {}
	local cost_share3 = {}
	local cost_motor = {}

	local cost_taxi_1 = {}
	local cost_taxi_2 = {}
	local cost_taxi={}
	local cost_SMS_1 = {}
	local cost_SMS_2 = {}
	local cost_SMS={}
	local cost_MRT = {}
--	local cost_AMOD = {}
--	local cost_AMOD_Pool = {}

	local d1={}
	local d2={}
	local central_dummy={}

	local tt_bus = {}
	local tt_private_bus = {}
	local tt_drive1 = {}
	local tt_share2 = {}
	local tt_share3 = {}
	local tt_motor = {}
	local tt_walk = {}
	local tt_taxi = {}
	local tt_SMS = {}
	local tt_bike = {}
	local tt_MRT = {}
	--local tt_AMOD = {}
	--local tt_AMOD_Pool={}
	
	local employment = {}
	local population = {}
	local area = {}
	local shop = {}
	local log = math.log
	local exp = math.exp

	local basefare_taxi = 4.46
	local fareperd_taxi = 0.47
	local fareperwait_taxi = 0.47
	
	local servicefee_SMS = 1.85
	local basefare_SMS = 2.1
	local farepred_SMS = 1.35
	local minfare_SMS = 6.85
	local farepermin_SMS = 0.21


	for i =1,917 do
		central_dummy[i] = dbparams:central_dummy(i)

		d1[i] = dbparams:walk_distance1(i)
		d2[i] = dbparams:walk_distance2(i)

		--walk
		tt_walk[i]=(d1[i]+d2[i])/5

		--bike
		tt_bike[i]=(d1[i]+d2[i])/20

		--PT
		cost_bus[i]=dbparams:cost_public_first(i)+dbparams:cost_public_second(i)
		tt_bus[i] = dbparams:tt_public_ivt_first(i)+ dbparams:tt_public_ivt_second(i)+ dbparams:tt_public_out_first(i)+dbparams:tt_public_out_second(i)
		
		--Private Bus
		cost_private_bus[i] = cost_bus[i]
		tt_private_bus[i] = tt_bus[i]
	
		--Car
		cost_drive1[i] = dbparams:cost_car_ERP_first(i)+dbparams:cost_car_ERP_second(i)+dbparams:cost_car_OP_first(i)+dbparams:cost_car_OP_second(i)+dbparams:cost_car_parking(i)
		cost_share2[i] = cost_drive1[i]/2
		cost_share3[i] = cost_drive1[i]/3

		tt_drive1[i] = dbparams:tt_car_ivt_first(i) + dbparams:tt_car_ivt_second(i) + 1.0/6
		tt_share2[i] = tt_drive1[i]
		tt_share3[i] = tt_drive1[i]

		--Motorcycle
		cost_motor[i] = 0.5*(dbparams:cost_car_ERP_first(i)+dbparams:cost_car_ERP_second(i)+dbparams:cost_car_OP_first(i)+dbparams:cost_car_OP_second(i))+0.65*dbparams:cost_car_parking(i)

		tt_motor[i] = tt_drive1[i]

		--Taxi
		cost_taxi_1[i] = basefare_taxi + fareperd_taxi *d1[i] + fareperwait_taxi * dbparams:tt_car_ivt_first(i)*60
		cost_taxi_2[i] = basefare_taxi + fareperd_taxi *d2[i] + fareperwait_taxi * dbparams:tt_car_ivt_second(i)*60
		cost_taxi[i] = cost_taxi_1[i]+cost_taxi_2[i]

		tt_taxi[i]= tt_drive1[i]

		--SMS
		cost_SMS_1[i] = servicefee_SMS + basefare_SMS +farepred_SMS*d1[i] + farepermin_SMS * dbparams:tt_car_ivt_first(i)*60
		cost_SMS_2[i] = servicefee_SMS + basefare_SMS +farepred_SMS*d2[i] + farepermin_SMS * dbparams:tt_car_ivt_second(i)*60
		cost_SMS[i] = math.max(cost_SMS_1[i],minfare_SMS)+math.max(cost_SMS_2[i],minfare_SMS)

		tt_SMS[i] = tt_drive1[i]

		--MRT
		cost_MRT[i]=dbparams:cost_mrt_first(i)+dbparams:cost_mrt_second(i)
		tt_MRT[i] = dbparams:tt_mrt_ivt_first(i)+ dbparams:tt_mrt_ivt_second(i) + dbparams:tt_mrt_out_first(i)+dbparams:tt_mrt_out_second(i)

		--AMOD
		--cost_AMOD[i] = cost_taxi[i]*0.5
		--tt_AMOD[i] = tt_drive1[i]

		--AMOD Pool
		--cost_AMOD_Pool[i] = 0.7*cost_AMOD[i]
		--tt_AMOD_Pool[i]= dbparams:tt_car_ivt_first(i) + dbparams:tt_car_ivt_second(i) + (d1[i]+d2[i])/2/60 + 1/6+1/10



		employment[i] = dbparams:employment(i)
		population[i] = dbparams:population(i)
		area[i] = dbparams:area(i)
		shop[i] = dbparams:shop(i)

	end


	local V_counter = 0

	--utility function for bus 1-917

	for i =1,917 do

		V_counter = V_counter + 1

		utility[V_counter] = beta_cons_PT + beta_cost*cost_bus[i] + 
		beta_tt_PT* tt_bus[i] + beta_cbd_PT * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end

	--utility function for private bus 1-917

	for i=1,917 do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_PB + 
		beta_tt_PT * tt_private_bus[i] + beta_cbd_PT * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end

	--utility function for drive1 1-917

	for i=1,917 do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_drive1 + beta_cost*cost_drive1[i] +
		beta_tt_drive1* tt_drive1[i] + beta_cbd_drive1 * central_dummy[i] +
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end

	--utility function for share2 1-917

	for i=1,917 do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_share2 + beta_cost* cost_share2[i]  +
		beta_tt_share2* tt_share2[i] + beta_cbd_share2 * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end

	--utility function for share3 1-917

	for i=1,917 do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_share3 + beta_cost*cost_share3[i] +
		beta_tt_share3* tt_share3[i] + beta_cbd_share3 * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end

	--utility function for motor 1-917

	for i=1,917 do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_motor + beta_cost*cost_motor[i] +
		beta_tt_motor* tt_motor[i] + beta_cbd_motor * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end

	--utility function for walk 1-917

	for i=1,917 do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_walk + 
		beta_tt_walk* tt_walk[i] + beta_cbd_notdrive * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end
	
		--utility function for taxi 1-917

	for i=1,917 do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_taxi + beta_cost * cost_taxi[i]+ 
		beta_tt_taxi *tt_taxi[i] + beta_cbd_taxi * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end

	--utility function for SMS 1-917

	for i=1,917 do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_SMS + beta_cost * cost_SMS[i] + 
		beta_tt_SMS* tt_SMS[i] + beta_cbd_SMS * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end

	--utility function for AMOD 1-917

	--for i=1,917 do

	--	V_counter = V_counter +1

		--utility[V_counter] = beta_cons_AMOD + beta_cost * cost_AMOD[i]+ 
		--beta_tt_AMOD *tt_AMOD[i] + beta_cbd_AMOD * central_dummy[i] + 
		--beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		--exp(beta_population)*population[i])

	--end

	--utility function for AMOD Pool 1-917

	--for i=1,917 do

	--	V_counter = V_counter +1

	--	utility[V_counter] = beta_cons_AMOD_Pool + beta_cost * cost_AMOD_Pool[i] + 
	--	beta_tt_AMOD_Pool * tt_AMOD_Pool[i] + beta_cbd_AMOD_Pool * central_dummy[i] + 
	--	beta_log * log(area[i]+exp(beta_employment)*employment[i]+
	--	exp(beta_population)*population[i])

	--end

	--utility function for bike 1-917
	for i=1,917 do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_bike + 
		beta_tt_bike* tt_bike[i] + beta_cbd_notdrive * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end

	--utility function for MRT 1-917

	for i =1,917 do

		V_counter = V_counter + 1

		utility[V_counter] = beta_cons_MRT + beta_cost*cost_MRT[i] + 
		beta_tt_MRT* tt_MRT[i] + beta_cbd_MRT * central_dummy[i] + 
		beta_log * log(area[i]+exp(beta_employment)*employment[i]+
		exp(beta_population)*population[i])

	end
	











end

--availability

--the logic to determine availability is the same with current implementation

local availability = {}

local function computeAvailabilities(params,dbparams)

	for i = 1, 917*11 do

		availability[i] = dbparams:availability(i)

	end
    ---set PB to unavailable
    for i = (917+1),917*2 do
        availability[i] = 0
    end

   -- ---set taxi to available
   -- for i = (917*7+1),917*8 do
   --     availability[i] = 1
   -- end

    ---set sms to unavailable
    for i = (917*8+1),917*9 do
        availability[i] = 0
    end
 	
--	--set AMOD availability
 --   for i = (917*7+1),917*8 do 
--	availability[i] = 1
  --  end

    --set AMOD_Pool availability
  --  for i = (917*8+1),917*9 do
--	availability[i] = 1
   -- end
	
    --set bike according to distance
    for i = (917*9+1),917*10 do
	if  availability[i-917*9] ==1 then
			if (dbparams:walk_distance1(i-917*9) > 25) then 
				availability[i] = 0 
			else
				availability[i] = 1
			end
	end
    end
    --set MRT availability
    for i = (917*10+1),917*11 do
    	if availability[i-917*10] == 1 then
    		if dbparams:tt_mrt_out_first(i-917*10) > 0.41 or dbparams:tt_mrt_out_second(i-917*10) >0.41
			then availability[i] = 0 
			else availability[i] = 1
		end
		--availability[i] = 0
	end 
    end

end


--scale

local scale = 1 --for all choices

-- function to call from C++ preday simulator

-- params and dbparams tables contain data passed from C++

-- to check variable bindings in params or dbparams, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp

function choose_tmdo(params,dbparams)

	computeUtilities(params,dbparams)

	computeAvailabilities(params,dbparams)

	local probability = calculate_probability("mnl", choice, utility, availability, scale)

	return make_final_choice(probability)

end

-- function to call from C++ preday simulator for logsum computation

-- params and dbparams tables contain data passed from C++

-- to check variable bindings in params or dbparams, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp

function compute_logsum_tmdo(params,dbparams)

	computeUtilities(params,dbparams)

	computeAvailabilities(params,dbparams)

	return compute_mnl_logsum(utility, availability)

end

