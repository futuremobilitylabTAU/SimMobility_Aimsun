--[[
Model - Mode/destination choice for intermediate stops
Type - logit
Based on tmdw by Siyu Li, Harish Loganathan
Created by Isabel Viegas on June 4, 2017
]]

-- all require statements do not work with C++. They need to be commented. The order in which lua files are loaded must be explicitly controlled in C++. 
--require "Logit"

--Estimated values for all betas
--Note: the betas that not estimated are fixed to zero.

--!! see the documentation on the definition of AM,PM and OP table!!

local num_zone = 917

local beta_cons_walk = -14.1 -2
local beta_cons_bike = -14.6 +1 +0.5  +1 +2 +5 +1
local beta_cons_drive1 = 12 +10 -5 -2
local beta_cons_share2 = 0.5 +1
local beta_cons_share3 = 0.3 -1 +0.5 +0.1
local beta_cons_PT = 2.3 +1
local beta_cons_PB = 0
local beta_cons_motor = 11 -8 -1 -1
local beta_cons_taxi = -15 -10 +5 +2 +2 +2
local beta_cons_SMS = 0                          
local beta_cons_MRT = 2.3 +1


local beta_cost = -0.04

local beta_tt_walk = -0.0844
local beta_tt_bike = -0.0903
local beta_tt_drive1 = -0.177
local beta_tt_share2 = -0.177
local beta_tt_share3 = -0.177
local beta_tt_PT = -0.0983 
local beta_tt_motor = -0.0903
local beta_tt_taxi = -0.177
local beta_tt_SMS = -0.177
local beta_tt_MRT = -0.0983 

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

local beta_cbd_work = 2.57 
local beta_cbd_edu = 0     
local beta_cbd_shop = 1.62          
local beta_cbd_other = 1.81

local beta_cbd_notdrive = -1.32
local beta_cbd_drive1 = -3.38
local beta_cbd_share2 = -2.84
local beta_cbd_share3 = -3.76
local beta_cbd_PT = -2.01
local beta_cbd_motor = (beta_cbd_notdrive+beta_cbd_PT)/2
local beta_cbd_taxi = (beta_cbd_notdrive+beta_cbd_PT)/2
local beta_cbd_SMS = (beta_cbd_notdrive+beta_cbd_PT)/2
local beta_cbd_rail_SMS = (beta_cbd_notdrive+beta_cbd_PT)/2
local beta_cbd_MRT = -2.01

local beta_log_work = 0.193
local beta_log_edu = 0
local beta_log_shop = 0.605
local beta_log_other = 0.385

local beta_employment = 3.27 +5
local beta_shop = 8.33
--choice set
local choice = {}
local C_counter = 0

-- regular trip 1
for i = 1, num_zone*11 do
	C_counter = C_counter + 1
	choice[i] = C_counter
end

-- regular trip 2
for i = num_zone*11+1, 2*num_zone*11 do
	C_counter = C_counter + 1
	choice[i] = C_counter
end


--utility

-- 1 for public bus; 2 for private bus; 3 for drive1;

-- 4 for shared2; 5 for shared3+; 6 for motor; 7 for walk; 8 for taxi; 9 for sms; 10 for bike; 11 for MRT

local utility = {}

local function computeUtilities(params,dbparams)
	local stoptype = dbparams.stop_type

	local work,edu,shop,other = 0.0,0.0,0.0,0.0

	if stoptype == 1 then

		work = 1.0

	elseif stoptype == 2 then

		edu = 1.0

	elseif stoptype == 3 then

	shop = 1.0

	elseif stoptype == 4 then

		other = 1.0

	end

	local female_dummy = params.female_dummy

	local income_id = params.income_id

	local income_cat =  {0,0.67, 1.4, 2.07, 2.61, 3.05, 3.47, 3.91, 4.4, 5.04, 6.15}
	local income_mid = income_cat[income_id]

	local missing_income = params.income_id >= 13 and 1 or 0

	local work_stop_dummy = dbparams.stop_type == 1 and 1 or 0

	local edu_stop_dummy = dbparams.stop_type == 2 and 1 or 0

	local SHOP_stop_dummy = dbparams.stop_type == 3 and 1 or 0

	local other_stop_dummy = dbparams.stop_type == 4 and 1 or 0

	--1 if the current modeled stop is on first half tour, 0 otherwise

	first_bound = dbparams.first_bound

	--1 if the current modeled stop is on second half tour, 0 otherwise

	second_bound = dbparams.second_bound

	--params.car_own_normal is from household table

	--imd use all cars (car_normal + car_offpeak) to calculate zero car...


	local cost_bus_first = {}
	local cost_bus_second = {}
       local cost_bus_car_first = {}
   	local cost_bus_car_second = {}
   	local cost_bus_mod_first = {}
   	local cost_bus_mod_second = {}
	local cost_private_bus_first = {}
	local cost_private_bus_second = {}
	local cost_drive1_first = {}
	local cost_drive1_second = {}
	local cost_share2_first = {}
	local cost_share2_second = {}
	local cost_share3_first = {}
	local cost_share3_second = {}
	local cost_motor_first = {}
	local cost_motor_second = {}
	local cost_taxi_first = {}
	local cost_taxi_second = {}

	local cost_SMS_first = {}
	local cost_SMS_second = {}
        local cost_MRT_first = {}
	local cost_MRT_second = {}

	local d1={}
	local d2={}

    --local pt_eta = params:random_parameter(1) --YdidyaTest
	local tt_bus_walk_first = {}
	local tt_bus_walk_second = {}
	local tt_bus_car_first = {}
	local tt_bus_car_second = {}
	local tt_bus_mod_first = {}
	local tt_bus_mod_second = {}
	local tt_private_bus_first = {}
	local tt_private_bus_second = {}
	local tt_drive1_first = {}
	local tt_drive1_second = {}
	local tt_share2_first = {}
	local tt_share2_second = {}
	local tt_share3_first = {}
	local tt_share3_second = {}
	local tt_motor_first = {}
	local tt_motor_second = {}
	local tt_walk_first = {}
	local tt_walk_second = {}
	local tt_taxi_first = {}
	local tt_taxi_second = {}
	local tt_SMS_first = {}
	local tt_SMS_second = {}
	local tt_bike_first = {}
	local tt_bike_second = {}
	local tt_MRT_first={}
	local tt_MRT_second={}
	local tt_MRT_walk_first={}
	local tt_MRT_walk_second={}

	local employment = {}
	local population = {}
	local area = {}
	local SHOP = {}
	local central_dummy = {}
	local log = math.log
	local exp = math.exp

	local tt_car_park = 5/60 * 2
	local tt_car_transfer = 3/60 * 2

	-- source: https://www.taxi-calculator.com/taxi-fare-austin/272
	local basefare_taxi = 2.5
	local fareperd_taxi = 1.5
	local fareperwait_taxi = 29/60
	
	-- uber price in san antonio area
	local servicefee_SMS = 2.04
	local basefare_SMS = 1.09
	local farepred_SMS = 0.91/1.60934
	local minfare_SMS = 6.87
	local farepermin_SMS = 0.19




	-- Common variables
	for i =1,num_zone do
		central_dummy[i] = dbparams:central_dummy(i)
		employment[i] = dbparams:employment(i)
		population[i] = dbparams:population(i)
		area[i] = dbparams:area(i)
		SHOP[i] = dbparams:shop(i)
	end

	--for i =1,num_zone do
	--	central_dummy[i] = dbparams:central_dummy(i)
	--	print(i)
	--	d1[i] = dbparams:walk_distance_first(i)
	--	d2[i] = dbparams:walk_distance_second(i)


	-- first trip
	for i =1,num_zone do
		--d_first[i] = dbparams:walk_distance_first(i)
		--print (d_first[i])
		--walk
		tt_walk_first[i]=dbparams:tt_walk_first(i)

		--bike
		tt_bike_first[i]=dbparams:tt_bike_first(i)

		--PT
		cost_bus_first[i]=dbparams:cost_public_first(i)
        	cost_bus_car_first[i]=dbparams:cost_public_first(i) -- dbparams:cost_pub_car_first(i)
      	cost_bus_mod_first[i]=dbparams:cost_public_first(i) -- dbparams:cost_pub_mod_first(i)
		tt_bus_walk_first[i] = dbparams:tt_pub_first(i)
		tt_bus_car_first[i] = dbparams:tt_pub_first(i) -- dbparams:tt_pub_car_first(i)
		tt_bus_mod_first[i] = dbparams:tt_pub_first(i) -- dbparams:tt_pub_mod_first(i)
		
		--Private Bus
		cost_private_bus_first[i] = cost_bus_first[i]
		tt_private_bus_first[i] = tt_bus_walk_first[i]
	
		--Car
		cost_drive1_first[i] = dbparams:cost_car_first(i)
		cost_share2_first[i] = dbparams:cost_share2_first(i)
		cost_share3_first[i] = dbparams:cost_share3_first(i)

		tt_drive1_first[i] = dbparams:tt_car_first(i) + tt_car_park + tt_car_transfer
		tt_share2_first[i] = dbparams:tt_car_first(i)
		tt_share3_first[i] = dbparams:tt_car_first(i)

		--Motorcycle
		cost_motor_first[i] = dbparams:cost_motor_first(i)
		tt_motor_first[i] = tt_drive1_first[i]

		--Taxi
		cost_taxi_first[i] = dbparams:cost_taxi_first(i)
		tt_taxi_first[i]= tt_drive1_first[i]

		--SMS
		cost_SMS_first[i] = dbparams:cost_sms_first(i)
		tt_SMS_first[i]= tt_drive1_first[i]
		
		
		--MRT

	      tt_MRT_first[i] = dbparams:tt_mrt_first(i)
	      cost_MRT_first[i]=dbparams:cost_mrt_first(i)
	      tt_MRT_walk_first[i]=dbparams:tt_mrt_first(i)


		

	end
	
	-- second trip
	for i =1,num_zone do
		--walk
		tt_walk_second[i]=dbparams:tt_walk_second(i)

		--bike
		tt_bike_second[i]=dbparams:tt_bike_second(i)

		--PT
		cost_bus_second[i]=dbparams:cost_public_second(i)
        cost_bus_car_second[i]=dbparams:cost_public_second(i) -- dbparams:cost_pub_car_second(i)
        cost_bus_mod_second[i]=dbparams:cost_public_second(i) -- dbparams:cost_pub_mod_second(i)
		tt_bus_walk_second[i] = dbparams:tt_pub_second(i)
		tt_bus_car_second[i] = dbparams:tt_pub_second(i) -- dbparams:tt_pub_car_second(i)
		tt_bus_mod_second[i] = dbparams:tt_pub_second(i) -- dbparams:tt_pub_mod_second(i)		
		
		--Private Bus
		cost_private_bus_second[i] = cost_bus_second[i]
		tt_private_bus_second[i] = tt_bus_walk_second[i]
	
		--Car
		cost_drive1_second[i] = dbparams:cost_car_second(i)
		cost_share2_second[i] = dbparams:cost_share2_second(i)
		cost_share3_second[i] = dbparams:cost_share3_second(i)

		tt_drive1_second[i] = dbparams:tt_car_second(i) + tt_car_park + tt_car_transfer
		tt_share2_second[i] = dbparams:tt_car_second(i)
		tt_share3_second[i] = dbparams:tt_car_second(i)

		--Motorcycle
		cost_motor_second[i] = dbparams:cost_motor_second(i)
		tt_motor_second[i] = tt_drive1_second[i]

		--Taxi
		cost_taxi_second[i] = dbparams:cost_taxi_second(i)
		tt_taxi_second[i]= tt_drive1_second[i]

		--SMS
		cost_SMS_second[i] = dbparams:cost_sms_second(i)
		tt_SMS_second[i]= tt_drive1_second[i]
		
		
			--MRT
	
	          tt_MRT_second[i] =dbparams:tt_mrt_second(i)	
		  cost_MRT_second[i]=dbparams:cost_mrt_second(i)
		  tt_MRT_walk_second[i]=dbparams:tt_mrt_second(i)
		--tt_MRT[i] = dbparams:cost_taxi_second(i)+ dbparams:cost_taxi_second(i)	
		
		
	end

--	
--	--	--walk
--	--	tt_walk[i]=(d1[i]+d2[i])/5/2
--
--		--bike
--		tt_bike[i]=(d1[i]+d2[i])/20/2
--
--		--PT
--		cost_bus[i]=dbparams:cost_public_first(i)
--		tt_bus[i] = dbparams:tt_pub_first(i)-- + dbparams:tt_public_out(i)
--		
--		--Private Bus
--		cost_private_bus[i] = cost_bus[i]
--		tt_private_bus[i] = tt_bus[i]
--	
--		--Car
--		cost_drive1[i] = dbparams:cost_car_first-- cost_car_ERP(i)+dbparams:cost_car_OP(i)+dbparams:cost_car_parking(i)
--		cost_share2[i] = cost_drive1[i]/2
--		cost_share3[i] = cost_drive1[i]/3
--
--		tt_drive1[i] = dbparams:tt_car_first --tt_car_ivt(i)+1.0/12
--		tt_share2[i] = tt_drive1[i]
--		tt_share3[i] = tt_drive1[i]
--
--		--Motorcycle
--		cost_motor[i] = 0.5*(dbparams:cost_car_ERP(i)+dbparams:cost_car_OP(i))+0.65*dbparams:cost_car_parking(i)
--
--		tt_motor[i] = tt_drive1[i]
--
--		--Taxi
--		cost_taxi_1[i] = basefare_taxi + fareperd_taxi *d1[i] + fareperwait_taxi * dbparams:tt_car_ivt(i)*60
--		cost_taxi_2[i] = basefare_taxi + fareperd_taxi *d2[i] + fareperwait_taxi * dbparams:tt_car_ivt(i)*60
--		cost_taxi[i] = (cost_taxi_1[i]+cost_taxi_2[i])/2
--
--		tt_taxi[i]= tt_drive1[i]
--
--		--SMS
--		cost_SMS_1[i] = servicefee_SMS + basefare_SMS +farepred_SMS*d1[i] + farepermin_SMS * dbparams:tt_car_ivt(i)*60
--		cost_SMS_2[i] = servicefee_SMS + basefare_SMS +farepred_SMS*d2[i] + farepermin_SMS * dbparams:tt_car_ivt(i)*60
--		cost_SMS[i] = (math.max(cost_SMS_1[i],minfare_SMS)+math.max(cost_SMS_2[i],minfare_SMS))/2
--
--		tt_SMS[i] = tt_drive1[i]
--
--		employment[i] = dbparams:employment(i)
--		population[i] = dbparams:population(i)
--		area[i] = dbparams:area(i)
--		SHOP[i] = dbparams:shop(i)
--
--	end
--
	--------------- compute utilities -------------------
	local V_counter = 0

	local log = math.log

	local exp= math.exp


--    Alternatives where second trip is fixed to tour mode (1, N_zones*Nmodes)

	--utility function for bus 1-917

	for i =1,num_zone do

		V_counter = V_counter + 1

		utility[V_counter] = beta_cons_PT + beta_cost* cost_bus_first[i] + 
		beta_tt_PT * tt_bus_walk_first[i] + 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_PT) * central_dummy[i]

	end


	--utility function for private bus 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_PB + 
		beta_tt_PT* tt_private_bus_first[i] + 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_PT) * central_dummy[i]
	end

	--utility function for drive1 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_drive1 + beta_cost* cost_drive1_first[i] +
		beta_tt_drive1*tt_drive1_first[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_drive1) * central_dummy[i]

	end

	--utility function for share2 1-917

	for i=1,num_zone do
		V_counter = V_counter +1

		utility[V_counter] = beta_cons_share2 + beta_cost* cost_share2_first[i] +
		beta_tt_share2 * tt_share2_first[i]+ 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_share2) * central_dummy[i]
	end

	--utility function for share3 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_share3 + beta_cost * cost_share3_first[i] +
		beta_tt_share3* tt_share3_first[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_share3) * central_dummy[i]
	end

	--utility function for motor 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_motor + beta_cost* cost_motor_first[i] + 
		beta_tt_motor* tt_motor_first[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_motor) * central_dummy[i]
	end

	--utility function for walk 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_walk + 
		beta_tt_walk* tt_walk_first[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_notdrive) * central_dummy[i]
	end

	--utility function for taxi 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_taxi + beta_cost * cost_taxi_first[i]+ 
		beta_tt_taxi* tt_taxi_first[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_taxi) * central_dummy[i]
	end

	--utility function for SMS 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_SMS + beta_cost * cost_SMS_first[i]+
		beta_tt_SMS* tt_SMS_first[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_SMS) * central_dummy[i]
	end

       --utility function for bike 1-917
	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_bike + 
		beta_tt_bike* tt_bike_first[i] + 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_notdrive) * central_dummy[i]
	end
	
	for i =1,num_zone do

		V_counter = V_counter + 1

		utility[V_counter] = beta_cons_MRT +  beta_cost* cost_MRT_first[i] + 
		beta_tt_MRT * tt_MRT_walk_first[i] + 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_PT) * central_dummy[i]

	end


	
	
	


	-------------------------------------------------------------------------------------
    --------------------------------- SECOND TRIP ---------------------------------------
    -------------------------------------------------------------------------------------
	--    Alternatives where first trip is fixed to tour mode (N_zones*Nmodes+1, 2*N_zones*Nmodes)

	--utility function for bus 1-917

	for i =1,num_zone do

		V_counter = V_counter + 1

		utility[V_counter] = beta_cons_PT + beta_cost* cost_bus_second[i] + 
		beta_tt_PT * tt_bus_walk_second[i] + 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_PT) * central_dummy[i]

	end


	--utility function for private bus 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_PB + 
		beta_tt_PT* tt_private_bus_second[i] + 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_PT) * central_dummy[i]
	end

	--utility function for drive1 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_drive1 + beta_cost* cost_drive1_second[i] +
		beta_tt_drive1*tt_drive1_second[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_drive1) * central_dummy[i]

	end

	--utility function for share2 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_share2 + beta_cost* cost_share2_second[i] +
		beta_tt_share2 * tt_share2_second[i]+ 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_share2) * central_dummy[i]
	end

	--utility function for share3 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_share3 + beta_cost * cost_share3_second[i] +
		beta_tt_share3* tt_share3_second[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_share3) * central_dummy[i]
	end

	--utility function for motor 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_motor + beta_cost* cost_motor_second[i] + 
		beta_tt_motor* tt_motor_second[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_motor) * central_dummy[i]
	end

	--utility function for walk 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_walk + 
		beta_tt_walk* tt_walk_second[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_notdrive) * central_dummy[i]
	end

	--utility function for taxi 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_taxi + beta_cost * cost_taxi_second[i]+ 
		beta_tt_taxi* tt_taxi_second[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_taxi) * central_dummy[i]
	end

	--utility function for SMS 1-917

	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_SMS + beta_cost * cost_SMS_second[i]+
		beta_tt_SMS* tt_SMS_second[i] +
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_SMS) * central_dummy[i]
	end

       --utility function for bike 1-917
	for i=1,num_zone do

		V_counter = V_counter +1

		utility[V_counter] = beta_cons_bike + 
		beta_tt_bike* tt_bike_second[i] + 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_notdrive) * central_dummy[i]
	end
	
	
	for i =1,num_zone do

		V_counter = V_counter + 1

		utility[V_counter] = beta_cons_MRT +  beta_cost* cost_MRT_second[i] + 
		beta_tt_MRT * tt_MRT_walk_second[i] + 
		(beta_log_work * work + beta_log_edu * edu + 
		beta_log_shop * shop + beta_log_other * other) * 
		log(area[i] + exp(beta_employment) * employment[i]+exp(beta_shop)*SHOP[i]) + 
		(beta_cbd_work * work + beta_cbd_edu * edu + beta_cbd_shop * shop + 
		beta_cbd_other * other+beta_cbd_PT) * central_dummy[i]

	end

	
	
	

end


--availability

--the logic to determine availability is the same with current implementation

local availability = {}

local function computeAvailabilities(params,dbparams)

	for i = 1, 917*11*2 do

		availability[i] = dbparams:availability(i)

	end

    ---set PB to unavailable
    for i = (917+1),917*2 do
        availability[i] = 0
    end
    for i = (12*917+1),917*13 do
        availability[i] = 0
    end

    --set taxi to available
    --for i = (917*7+1),917*8 do
    --    availability[i] = 1
    --end
    --set sms to unavailable
    
    for i = (917*8+1),917*9 do
        availability[i] = 0
    end
    for i = (917*19+1),917*20 do
        availability[i] = 0
    end
    
    ----set mrt to unavailable
    --
    for i = (917*10+1),917*11 do
        availability[i] = 0
    end
    for i = (917*21+1),917*22 do
        availability[i] = 0
    end
    
--    --set bike according to distance
--    for i = (917*9+1),917*10 do
--	if availability[i-917*9] == 1 then
--    		if dbparams:walkdistance_first(i-917*9) > 25 then 
--			availability[i] = 0 
--		else 
--			availability[i] = 1
--		end
--	end
--    end
end

--scale

local scale=1

-- function to call from C++ preday simulator

-- params and dbparams tables contain data passed from C++

-- to check variable bindings in params or dbparams, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp

function choose_imd(params,dbparams)
	
	computeUtilities(params,dbparams)

	computeAvailabilities(params,dbparams)

	local probability = calculate_probability("mnl", choice, utility, availability, scale)

	return make_final_choice(probability)
	
end

