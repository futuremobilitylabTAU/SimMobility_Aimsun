--[[
Model - Mode choice for work tour to usual location
Based on tmw.lua by Siyu Li, Harish Loganathan
]]

local cons_walk = 1.75  -1 +0.5 -0.2 -0.1  +0.06      
local cons_bike = -2.2   +0.1 +0.1 +0.2  +0.1                     
local cons_drive1 = 1.25 -0.2 +0.1 +0.2 +0.5 -0.4
local cons_share2 = 1.75    -0.2 -0.5             
local cons_share3 = 1.3 -1 +0.8 -0.4 -0.2 +0.1
local cons_PT = -2.71 +0.71 +1 -0.2 -0.2 -0.1
local cons_PB = -0.75
local cons_motor = 3.2 -3 -1 -0.5
local cons_taxi = -3.65 +0.1
local cons_SMS = 0  
local cons_MRT = 0                                

local beta_tt_walk = -0.0814
local beta_tt_bike = -0.0698
local beta_tt_drive1 = -0.0474
local beta_tt_share2 = -0.0599
local beta_tt_share3 = -0.0617
local beta_tt_PT = -0.00436
local beta_tt_motor = -0.0698
local beta_tt_taxi = -0.0474
local beta_tt_SMS = -0.0474
local beta_tt_MRT = -0.00436

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

local beta_cost = -0.0432

local beta_central_walk = 2.49
local beta_central_bike = 1.5
local beta_central_drive1 = 0
local beta_central_share2 = 0
local beta_central_share3 = 0
local beta_central_PT = 2.12
local beta_central_motor = 0
local beta_central_taxi = beta_central_PT
local beta_central_SMS= beta_central_PT
local beta_central_rail_SMS= beta_central_PT
local beta_central_MRT = 2.12

local beta_parttime_walk = 0
local beta_parttime_bike = 0
local beta_parttime_drive1 = 0
local beta_parttime_share2 = 0.522
local beta_parttime_share3 = -0.336
local beta_parttime_PT = -0.729
local beta_parttime_motor = 0
local beta_parttime_taxi = 0
local beta_parttime_SMS = 0
local beta_parttime_rail_SMS = 0
local beta_parttime_MRT = -0.729

local beta_preschool_walk = 0.617
local beta_preschool_bike = 0
local beta_preschool_drive1 = 0
local beta_preschool_share2 = 1.28
local beta_preschool_share3 = 1.40
local beta_preschool_PT = -0.736
local beta_preschool_motor = 0
local beta_preschool_taxi = 0
local beta_preschool_SMS = 0
local beta_preschool_rail_SMS = 0
local beta_preschool_MRT = -0.736

local beta_undergraduate_walk = 0
local beta_undergraduate_bike = 1.49
local beta_undergraduate_drive1 = 0
local beta_undergraduate_share2 = -0.457
local beta_undergraduate_share3 = -1.96
local beta_undergraduate_PT = 0
local beta_undergraduate_motor = 0
local beta_undergraduate_taxi = 0
local beta_undergraduate_SMS = 0
local beta_undergraduate_rail_SMS = 0
local beta_undergraduate_MRT = 0

local beta_female_walk = 0
local beta_female_bike = -1.27
local beta_female_drive1 = 0
local beta_female_share2 = 0
local beta_female_share3 = 0
local beta_female_PT = -0.314
local beta_female_motor = 0
local beta_female_taxi = 0
local beta_female_SMS = 0
local beta_female_rail_SMS = 0
local beta_female_MRT = -0.314

local beta_LIC_walk = 1.32
local beta_LIC_bike = 0
local beta_LIC_drive1 = 0
local beta_LIC_share2 = 1.46
local beta_LIC_share3 = 0
local beta_LIC_PT = 0
local beta_LIC_motor = 0
local beta_LIC_taxi = 0
local beta_LIC_SMS = 0 
local beta_LIC_rail_SMS = 0
local beta_LIC_MRT = 0

local beta_TRANS_walk = 1.26
local beta_TRANS_bike = 0
local beta_TRANS_drive1 = 0
local beta_TRANS_share2 = 0
local beta_TRANS_share3 = 0
local beta_TRANS_PT = 1.20
local beta_TRANS_motor = 0
local beta_TRANS_taxi = 0
local beta_TRANS_SMS = 0
local beta_TRANS_rail_SMS = beta_TRANS_PT
local beta_TRANS_MRT = 1.20

local beta_zerocar_walk = 0
local beta_zerocar_bike = 1.05
local beta_zerocar_drive1 = 0
local beta_zerocar_share2 = -1.20
local beta_zerocar_share3 = 0
local beta_zerocar_PT = 0.761
local beta_zerocar_motor = 0
local beta_zerocar_taxi = beta_zerocar_PT
local beta_zerocar_SMS = beta_zerocar_PT
local beta_zerocar_rail_SMS = beta_zerocar_PT
local beta_zerocar_MRT = 0.761

local beta_onecar_walk = 1.13
local beta_onecar_bike = 1.40
local beta_onecar_drive1 = 0
local beta_onecar_share2 = 0.272
local beta_onecar_share3 = 0.843
local beta_onecar_PT = 0.600
local beta_onecar_motor = 0
local beta_onecar_taxi = beta_onecar_PT
local beta_onecar_SMS = beta_onecar_PT
local beta_onecar_rail_SMS = beta_onecar_PT
local beta_onecar_MRT = 0.600

local beta_twocar_walk = 0.360
local beta_twocar_bike = 0.767
local beta_twocar_drive1 = 0
local beta_twocar_share2 = 0.459
local beta_twocar_share3 = 1.08
local beta_twocar_PT = 0.376
local beta_twocar_motor = 0
local beta_twocar_taxi = beta_twocar_PT
local beta_twocar_SMS = beta_twocar_PT
local beta_twocar_rail_SMS = beta_onecar_PT
local beta_twocar_MRT = 0.376

local beta_threepluscar_walk = 0
local beta_threepluscar_bike = 0
local beta_threepluscar_drive1 = 0
local beta_threepluscar_share2 = 0
local beta_threepluscar_share3 = 0
local beta_threepluscar_PT = 0
local beta_threepluscar_motor = 0
local beta_threepluscar_taxi = 0
local beta_threepluscar_SMS = 0
local beta_threepluscar_rail_SMS = 0
local beta_threepluscar_MRT = 0

local choice = {

		1,

		2,

		3,

		4,

		5,

		6,

		7,

		8,

		9,

		10,
		
		11
}

local modes = {['BusTravel'] = 1 , ['PrivateBus'] =2 ,
  ['Car'] = 3,  ['Car_Sharing_2'] = 4,['Car_Sharing_3'] =5,
  ['Motorcycle'] = 6,['Walk'] = 7, ['Taxi'] = 8 , ['SMS'] = 9, 
  ['Bike'] = 10 , ['MRT'] = 11}


local utility = {}
local function computeUtilities(params,dbparams)

	local CBD = dbparams.central_dummy


	local female_dummy = params.female_dummy
	local income_id = params.income_id
	--local income_cat = {500,1250,1750,2250,2750,3500,4500,5500,6500,7500,8500,0,99999,99999}
    	--local income_mid = {0.75,2,3,4.25,6.25,8.75,12.5,20}
	local income_mid =  {0,0.67, 1.4, 2.07, 2.61, 3.05, 3.47, 3.91, 4.4, 5.04, 6.15}
	local INCOME = income_mid[income_id]
	local missing_income = (params.income_id >= 13) and 1 or 0

	local age_id = params.age_id
	local age_over_15 = age_id >= 3 and 1 or 0
	local student_type_id = params.student_type_id
	local university_student = student_type_id == 6 and 1 or 0


	--local zero_car,one_plus_car,two_plus_car,three_plus_car, zero_motor,one_plus_motor,two_plus_motor,three_plus_motor = 0,0,0,0,0,0,0,0
	local zerocar,onecar,twocar,threepluscar, zero_motor,one_plus_motor,two_plus_motor,three_plus_motor = 0,0,0,0,0,0,0,0
	local veh_own_cat = params.vehicle_ownership_category

	if veh_own_cat == 0  then
		zerocar = 1--zero_car = 1
	end
	if veh_own_cat == 3 or veh_own_cat == 4 or veh_own_cat == 5  then
		onecar =1-- one_plus_car = 1
	end
	if veh_own_cat == 5  then
		twocar=1--two_plus_car = 1
	end
	if veh_own_cat == 5  then
		threepluscar=1 --three_plus_car = 1
	end

	if veh_own_cat == 0 or veh_own_cat == 3  then
		zero_motor = 1
	end
	if veh_own_cat == 1 or veh_own_cat == 2 or veh_own_cat == 4 or veh_own_cat == 5  then
		one_plus_motor = 1
	end
	if veh_own_cat == 1 or veh_own_cat == 2 or veh_own_cat == 4 or veh_own_cat == 5  then
		two_plus_motor = 1
	end
	if veh_own_cat == 1 or veh_own_cat == 2 or veh_own_cat == 4 or veh_own_cat == 5  then
		three_plus_motor = 1
	end

	local person_type_id = params.person_type_id 

	local age_id = params.age_id


	local student_dummy = params.student_dummy
	local LIC = params.has_driving_licence
	local studentTypeId = params.studentTypeId
	local transit = params.vanbus_license
	local fixedworktime = params.fixed_work_hour
	local female = 0
	if female_dummy == 0 then

		female = 1

	end


	local LIC = 0

	if license == true then

		LIC = 1

	end

	local TRANS = 0

	if transit == true then

		TRANS = 1

	end

	local infant = 0
	local fulltime,parttime,student,homemaker,retired,unemployed,preschool,studentK8,student912,undergraduate,graduate,otherstudent = 0,0,0,0,0,0,0,0,0,0,0,0
	if person_type_id == 1 then
		fulltime = 1
	elseif person_type_id == 2 then 
		parttime = 1
	-- elseif person_type_id == 3 then
	-- 	student = 1
	elseif person_type_id == 4 then 
		homemaker = 1
	elseif person_type_id == 5 then
		retired = 1
	elseif person_type_id == 6 then
		unemployed = 1
	end

	if studentTypeId == 1 then
		preschool = 1
	elseif studentTypeId == 2 then
		studentK8 = 1
	elseif studentTypeId == 3 then
		student912 = 1
	elseif studentTypeId == 4 then
		undergraduate = 1
	elseif studentTypeId == 5 then
		graduate = 1
	elseif studentTypeId == 6 then
		otherstudent = 1
	end 

	student = studentTypeId ==0 and 0 or 1

	local age_id = params.age_id

	-- age group related variables

	local age20,age2025,age2635,age3650,age5165,age65,missingage = 0,0,0,0,0,0,0

	if age_id < 4 then

		age20 = 1

	elseif age_id == 4 then

		age2025 = 1

	elseif age_id == 5 or age_id == 6 then

		age2635 = 1

	elseif age_id == 7 or age_id == 8 or age_id == 9 then

		age3650 = 1

	elseif age_id == 10 or age_id == 11 or age_id == 12 then

		age5165 = 1

	elseif age_id > 12 then

		age65 = 1

	end

	local d1 = dbparams.walk_distance1
	local d2 = dbparams.walk_distance2

	--walk
	local tt_walk=(d1+d2)/5

	--bike
	local tt_bike=(d1+d2)/20

	--PT
	local cost_bus=dbparams.cost_public_first+dbparams.cost_public_second

	local tt_bus_ivt=dbparams.tt_public_ivt_first+dbparams.tt_public_ivt_second
	local tt_bus_wait=dbparams.tt_public_waiting_first+dbparams.tt_public_waiting_second
	local tt_bus_walk=dbparams.tt_public_walk_first+dbparams.tt_public_walk_second
	local tt_bus_all=tt_bus_ivt+tt_bus_wait+tt_bus_walk

	--Private Bus
	local tt_privatebus_all = tt_bus_all
	if tt_bus_ivt == 0 then
		tt_privatebus_all = (d1+d2)/30
	end
	--Car
	local cost_cardriver=dbparams.cost_car_ERP_first+dbparams.cost_car_ERP_second+dbparams.cost_car_OP_first+dbparams.cost_car_OP_second+dbparams.cost_car_parking
	local cost_carpassenger=cost_cardriver

	local tt_cardriver_ivt=dbparams.tt_ivt_car_first+dbparams.tt_ivt_car_second
	local tt_cardriver_out=1.0/6
	local tt_cardriver_all=tt_cardriver_ivt+tt_cardriver_out
	local tt_carpassenger_all = tt_cardriver_all

	--Motorcycle
	local cost_motor=0.5*(dbparams.cost_car_ERP_first+dbparams.cost_car_ERP_second+dbparams.cost_car_OP_first+dbparams.cost_car_OP_second)+0.65*dbparams.cost_car_parking

	local tt_motor_all = tt_cardriver_all
	
	--Taxi
	local basefare_taxi = 4.46
	local fareperd_taxi = 0.47
	local fareperwait_taxi = 0.47
	local cost_taxi_1 = basefare_taxi + fareperd_taxi *d1 + fareperwait_taxi * dbparams.tt_ivt_car_first*60
	local cost_taxi_2 = basefare_taxi + fareperd_taxi *d2 + fareperwait_taxi * dbparams.tt_ivt_car_second*60
	local cost_taxi = cost_taxi_1+cost_taxi_2

	local tt_taxi_all=tt_cardriver_all

	--SMS
	local servicefee_SMS = 1.85
	local basefare_SMS = 2.1
	local farepred_SMS = 1.35
	local minfare_SMS = 6.85
	local farepermin_SMS = 0.21
	local cost_SMS_1 = servicefee_SMS + basefare_SMS +farepred_SMS*d1 + farepermin_SMS * dbparams.tt_ivt_car_first*60
	local cost_SMS_2 = servicefee_SMS + basefare_SMS +farepred_SMS*d2 + farepermin_SMS * dbparams.tt_ivt_car_second*60
	local cost_SMS = math.max(cost_SMS_1,minfare_SMS)+math.max(cost_SMS_2,minfare_SMS)

	local tt_SMS_all=tt_cardriver_all

	--MRT

	local cost_mrt=dbparams.cost_mrt_first+dbparams.cost_mrt_second
	

	local tt_mrt_wait=dbparams.tt_mrt_waiting_first+dbparams.tt_mrt_waiting_second
	local tt_mrt_walk=dbparams.tt_mrt_walk_first+dbparams.tt_mrt_walk_second
	local tt_mrt_ivt=dbparams.tt_mrt_ivt_first+dbparams.tt_mrt_ivt_second
	local tt_mrt_all=tt_mrt_ivt+tt_mrt_wait+tt_mrt_walk

	--bus
	utility[1] = cons_PT + beta_tt_PT * (tt_bus_ivt + tt_bus_walk + tt_bus_wait) +
	beta_cost * cost_bus + beta_central_PT * CBD + 
	beta_parttime_PT * parttime +
	beta_female_PT * female +
	beta_TRANS_PT * TRANS + beta_LIC_PT * LIC +beta_zerocar_PT * zerocar +
	beta_onecar_PT * onecar + beta_twocar_PT * twocar +
	beta_threepluscar_PT * threepluscar +
	beta_preschool_PT * preschool +
	beta_undergraduate_PT * undergraduate 

	--private bus
	utility[2] = cons_PB + beta_tt_PT * tt_privatebus_all + 
	beta_central_PT * CBD + 
	beta_parttime_PT * parttime +
	beta_female_PT * female +
	beta_TRANS_PT * TRANS + beta_LIC_PT * LIC +beta_zerocar_PT * zerocar +
	beta_onecar_PT * onecar + beta_twocar_PT * twocar +
	beta_threepluscar_PT * threepluscar +
	beta_preschool_PT * preschool +
	beta_undergraduate_PT * undergraduate 
	--drive 1
	utility[3] = cons_drive1 + beta_tt_drive1 * tt_cardriver_all + 
	beta_cost * cost_cardriver + beta_central_drive1 * CBD +
	beta_parttime_drive1 * parttime +
	beta_female_drive1 * female +
	beta_TRANS_drive1 * TRANS + beta_LIC_drive1 * LIC +beta_zerocar_drive1 * zerocar +
	beta_onecar_drive1 * onecar + beta_twocar_drive1 * twocar +
	beta_threepluscar_drive1 * threepluscar +
	beta_preschool_drive1 * preschool +
	beta_undergraduate_drive1 * undergraduate 
	--share 2
	utility[4] = cons_share2 + beta_tt_share2 * tt_carpassenger_all + 
	beta_cost * cost_carpassenger/2.0  + beta_central_share2 * CBD + 
	beta_parttime_share2 * parttime +
	beta_female_share2 * female +
	beta_TRANS_share2 * TRANS + beta_LIC_share2 * LIC +beta_zerocar_share2 * zerocar +
	beta_onecar_share2 * onecar + beta_twocar_share2 * twocar +
	beta_threepluscar_share2 * threepluscar +
	beta_preschool_share2 * preschool +
	beta_undergraduate_share2 * undergraduate 
	--share 3
	utility[5] = cons_share3+ beta_tt_share3 * tt_carpassenger_all + 
	beta_cost * cost_carpassenger/3.0  + beta_central_share3 * CBD + 
	beta_parttime_share3 * parttime +
	beta_female_share3 * female +
	beta_TRANS_share3 * TRANS + beta_LIC_share3 * LIC +beta_zerocar_share3 * zerocar +
	beta_onecar_share3 * onecar + beta_twocar_share3 * twocar +
	beta_threepluscar_share3 * threepluscar +
	beta_preschool_share3 * preschool +
	beta_undergraduate_share3 * undergraduate 
	--motor
	utility[6] = cons_motor + beta_tt_motor* tt_motor_all + 
	beta_cost * cost_motor + beta_central_motor * CBD + 
	beta_parttime_motor * parttime +
	beta_female_motor * female +
	beta_TRANS_motor * TRANS + beta_LIC_motor * LIC +beta_zerocar_motor * zerocar +
	beta_onecar_motor * onecar + beta_twocar_motor * twocar +
	beta_threepluscar_motor * threepluscar +
	beta_preschool_motor * preschool +
	beta_undergraduate_motor * undergraduate 
	--walk
	utility[7] = cons_walk  + beta_tt_walk * tt_walk + beta_central_walk * CBD+ 
	beta_parttime_walk * parttime +
	beta_female_walk * female +
	beta_TRANS_walk * TRANS + beta_LIC_walk * LIC +beta_zerocar_walk * zerocar +
	beta_onecar_walk * onecar + beta_twocar_walk * twocar +
	beta_threepluscar_walk * threepluscar +
	beta_preschool_walk * preschool +
	beta_undergraduate_walk * undergraduate 
	--taxi
	utility[8] = cons_taxi+ beta_tt_taxi * tt_taxi_all + 
	beta_cost * cost_taxi + beta_central_taxi * CBD + 
	beta_female_taxi * female +
	beta_TRANS_taxi * TRANS + beta_LIC_taxi * LIC +beta_zerocar_taxi * zerocar +
	beta_onecar_taxi * onecar + beta_twocar_taxi * twocar +
	beta_threepluscar_taxi * threepluscar +
	beta_preschool_taxi * preschool +
	beta_undergraduate_taxi * undergraduate 
	--SMS
	utility[9] = cons_SMS + beta_tt_SMS * tt_SMS_all + 
	beta_cost * cost_SMS + beta_central_SMS * CBD +
	beta_female_SMS * female +
	beta_TRANS_SMS * TRANS + beta_LIC_SMS * LIC +beta_zerocar_SMS * zerocar +
	beta_onecar_SMS * onecar + beta_twocar_SMS * twocar +
	beta_threepluscar_SMS * threepluscar +
	beta_preschool_SMS * preschool +
	beta_undergraduate_SMS * undergraduate  
	--bike
	utility[10] = cons_bike + beta_tt_bike * tt_bike + 
	beta_central_bike * CBD + 
	beta_female_bike * female +
	beta_TRANS_bike * TRANS + beta_LIC_bike * LIC +beta_zerocar_bike * zerocar +
	beta_onecar_bike * onecar + beta_twocar_bike * twocar +
	beta_threepluscar_bike * threepluscar +
	beta_preschool_bike * preschool +
	beta_undergraduate_bike * undergraduate 
	--mrt
	utility[11] = cons_MRT + beta_tt_MRT * tt_mrt_all +
	beta_cost * cost_mrt + 
	beta_central_MRT * CBD + 
	beta_parttime_MRT * parttime +
	beta_female_MRT * female +
	beta_TRANS_MRT * TRANS + beta_LIC_MRT * LIC +beta_zerocar_MRT * zerocar +
	beta_onecar_MRT * onecar + beta_twocar_MRT * twocar +
	beta_threepluscar_MRT * threepluscar +
	beta_preschool_MRT * preschool +
	beta_undergraduate_MRT * undergraduate 
end

--availability

--the logic to determine availability is the same with current implementation

local availability = {}

local function computeAvailabilities(params,dbparams)
	-- the PB is available to all preschool, k8 and 912 student
	-- for grad/undergrad it is available as PT
	local studentTypeId = params.studentTypeId
	local PB_av = dbparams:getModeAvailability(modes.PrivateBus) or (studentTypeId <=3)
	if studentTypeId == 6 then
		PB_av = 0
	end

 	--set bike according to distance
	-- local bike_av = dbparams:getModeAvailability(modes.Motorcycle)
        local bike_av = 1
	if dbparams.walk_distance1 > 25 then bike_av = 0 end
	
	-- max 25 min walk to station
	--local mrt_av = dbparams:getModeAvailability(modes.MRT)
	--if dbparams.tt_mrt_walk_first > 0.41 or dbparams.tt_mrt_walk_second > 0.41 then mrt_av = 0 end
	mrt_av = 0
	
	
	sms_av = 0 	
	taxi_av = 1

 	availability = {
	dbparams:getModeAvailability(modes.BusTravel),
		PB_av,
		dbparams:getModeAvailability(modes.Car),
		dbparams:getModeAvailability(modes.Car_Sharing_2),
		dbparams:getModeAvailability(modes.Car_Sharing_3),
		dbparams:getModeAvailability(modes.Motorcycle),
		dbparams:getModeAvailability(modes.Walk),
		--dbparams:getModeAvailability(modes.Taxi),
		taxi_av,
		--dbparams:getModeAvailability(modes.SMS),
		sms_av,
		bike_av,
		mrt_av
}


end


-- function to call from C++ preday simulator

-- params and dbparams tables contain data passed from C++

-- to check variable bindings in params or dbparams, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp
local function output_decisions(user_id,utility,availability,probability)
    local filename ='tme_base.csv'
    sep = ','
    local file = assert(io.open(filename, "a"))
    file:write(user_id)
    for i,v in pairs(utility) do
       file:write(sep)
       file:write(v)
    end
    for i,v in pairs(availability) do
       file:write(sep)
       file:write(v)
    end
    for i,v in pairs(probability) do
       file:write(sep)
       file:write(v)
    end
    file:write('\n')
    file:close()
    return
end
scale = 1
function choose_tme(params,dbparams)
	computeUtilities(params,dbparams)
	computeAvailabilities(params,dbparams)
	local probability = calculate_probability("mnl", choice, utility, availability, scale)
	output_decisions(params.person_id,utility,availability,probability)
	return make_final_choice(probability)

end

-- function to call from C++ preday simulator for logsums computation

-- params and dbparams tables contain data passed from C++

-- to check variable bindings in params or dbparams, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp

function compute_logsum_tme(params,dbparams)

	computeUtilities(params,dbparams) 

	computeAvailabilities(params,dbparams)

	return compute_mnl_logsum(utility, availability)

end

