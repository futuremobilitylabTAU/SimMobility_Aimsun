--[[
Model - intermediate stop generation
Type - MNL
Based on - isg by Siyu Li, Harish Loganathan
Created on June 8, 2017 by Isabel Viegas
]]

-- require statements do not work with C++. They need to be commented. The order in which lua files are loaded must be explicitly controlled in C++. 
--require "Logit"

--Estimated values for all betas
--Note= the betas that not estimated are fixed to zero.

local beta_cons_work = -1 -0.2   -0.2 -1 +0.5  -0.1                                  --  -1.24
local beta_cons_edu = -7.2                                 --  -1.87
local beta_cons_shop = -5.12 -0.5 +0.4 +0.1 +0.1 +0.05 -0.01
local beta_cons_other = -4.768 +0.038 -0.005 -0.01                        --  -6.08-0.01
local beta_cons_quit = 3 + 2 +4 +1 -0.1 +0.09  +0.1  +0.2 +0.1                                  --  8.85    -- base


local beta_female_work = -0.00165
local beta_female_edu = 0.113
local beta_female_shop = 0.131
local beta_female_other = 0.116

local beta_window_work_inbound = -0.33 +0.1 -0.1
local beta_window_edu_inbound = -1.19 +0.3 +0.2 +0.2 +0.2 +0.5 +0.2
local beta_window_shop_inbound = 0.03
local beta_window_other_inbound = 0.073

local beta_window_work_outbound = 0.35
local beta_window_edu_outbound = 0.85 - 0.1 -0.2 -0.2 -0.2 +0.1 +0.05 +0.05
local beta_window_shop_outbound = -0.033
local beta_window_other_outbound = -0.025

local beta_window_1_inbound =13.12       
local beta_window_2_inbound = 13.628     
local beta_window_3_inbound =-1.346 
local beta_window_1_outbound = 14.07 
local beta_window_2_outbound = 1.481  +10+1.5+1 +1 +0.7 -0.2       
local beta_window_3_outbound = 1.25                                      +0.5 

local beta_prime_work_work = 0       -2-1
local beta_prime_work_edu = 0 
local beta_prime_work_shop = 0
local beta_prime_work_other = 0

local beta_prime_edu_work = -1.09 -6
local beta_prime_edu_edu = -0.158
local beta_prime_edu_shop = -0.890
local beta_prime_edu_other= -0.607

local beta_prime_shop_work = -3.04 -6
local beta_prime_shop_edu = 2.23
local beta_prime_shop_shop = 0.148
local beta_prime_shop_other = 0.183


local beta_prime_other_work = -2.78 -6
local beta_prime_other_edu = -1.84
local beta_prime_other_shop = 0.406
local beta_prime_other_other = 0.352


--choice set
--1 for work; 2 for edu; 3 for shopping; 4 for other; 5 for quit
local choice = {}
choice["make"] = {1,2,3,4}
choice["quit"] = {5}

local utility = {}
local function computeUtilities(params,dbparams)

	-- NOT USED YET
	-- local student_dummy = params.student_dummy
	local female = params.female_dummy
	-- print("female: ", female)
	-- local worker_dummy = params.worker_dummy
	-- local driver_dummy = dbparams.driver_dummy
	-- local passenger_dummy = dbparams.passenger_dummy
	-- local public_dummy = dbparams.public_dummy
	-- local distance = dbparams.distance
	-- local log_constant = 0.0001
	-- local worklogsum = 0
	-- local edulogsum = 0
	-- local shoplogsum = 0
	-- local otherlogsum = 0
	-- p_700a_930a = dbparams.p_700a_930a
	-- p_930a_1200a = dbparams.p_930a_1200a 
	-- p_300p_530p = dbparams.p_300p_530p
	-- p_530p_730p = dbparams.p_530p_730p
	-- p_730p_1000p = dbparams.p_730p_1000p
	-- p_1000p_700a = dbparams.p_1000p_700a
	local first_stop = dbparams.first_stop
	-- print("first_stop")
	local second_stop = dbparams.second_stop
	-- print("second_stop")
	local three_plus_stop = dbparams.three_plus_stop
	-- print("three_plus_stop")


	-- primary activity
	local tour_type = dbparams.tour_type
	-- print("tour_type:", tour_type)

	local pwork,pedu,pshop,pother = 0,0,0,0

	if tour_type == 1 then
		pwork = 1
	end

	if tour_type == 2 then
		pedu = 1
	end

	if tour_type == 3 then
		pshop = 1
	end

	if tour_type == 4 then
		pother = 1
	end



	local inbound_window = dbparams.time_window_first_bound
	local outbound_window = dbparams.time_window_second_bound 

	-- print("inbound_window: ",inbound_window,", outbound_window: ",outbound_window)

	local inbound = dbparams.first_bound
	local outbound = dbparams.second_bound

	-- print("inbound: ", inbound, ", outbound: ", outbound)

	-- print("stops: ", first_stop, " ", second_stop, " ", three_plus_stop)
	local stop1,stop2,stop3 = 0,0,0
	if first_stop == 1 then
		stop1 = 1
	end
	if second_stop == 1 then
		stop2 = 1
	end
	if three_plus_stop == 1 then
		stop3 = 1
	end

	-- print("stops: ", stop1, " ", stop2, " ", stop3)


	utility[1] = beta_cons_work +
	inbound_window * beta_window_work_inbound * inbound + outbound_window * beta_window_work_outbound * outbound +
	beta_prime_work_work * pwork + 
	beta_prime_edu_work * pedu + 
	beta_prime_shop_work * pshop + 
	beta_prime_other_work * pother+
	inbound * (beta_window_1_inbound * stop1 + beta_window_2_inbound * stop2 + beta_window_3_inbound * stop3) +
	outbound * (beta_window_1_outbound * stop1 + beta_window_2_outbound * stop2 + beta_window_3_outbound * stop3) +
	female * beta_female_work

	utility[2] = beta_cons_edu +
	inbound_window * beta_window_edu_inbound * inbound + outbound_window * beta_window_edu_outbound * outbound +
	beta_prime_work_edu * pwork + 
	beta_prime_edu_edu * pedu + 
	beta_prime_shop_edu * pshop + 
	beta_prime_other_edu * pother +
	inbound * (beta_window_1_inbound * stop1 + beta_window_2_inbound * stop2 + beta_window_3_inbound * stop3) +
	outbound * (beta_window_1_outbound * stop1 + beta_window_2_outbound * stop2 + beta_window_3_outbound * stop3) +
	female * beta_female_edu

	utility[3] = beta_cons_shop +
	inbound_window * beta_window_shop_inbound * inbound + outbound_window * beta_window_shop_outbound * outbound +
	beta_prime_work_shop * pwork + 
	beta_prime_edu_shop * pedu + 
	beta_prime_shop_shop * pshop + 
	beta_prime_other_shop * pother +
	inbound * (beta_window_1_inbound * stop1 + beta_window_2_inbound * stop2 + beta_window_3_inbound * stop3) +
	outbound * (beta_window_1_outbound * stop1 + beta_window_2_outbound * stop2 + beta_window_3_outbound * stop3) +
	female * beta_female_shop

	utility[4] = beta_cons_other +
	inbound_window * beta_window_other_inbound * inbound + outbound_window * beta_window_other_outbound * outbound +
	beta_prime_work_other * pwork + 
	beta_prime_edu_other * pedu + 
	beta_prime_shop_other * pshop + 
	beta_prime_other_other * pother +
	inbound * (beta_window_1_inbound * stop1 + beta_window_2_inbound * stop2 + beta_window_3_inbound * stop3) +
	outbound * (beta_window_1_outbound * stop1 + beta_window_2_outbound * stop2 + beta_window_3_outbound * stop3) +
	female * beta_female_other

	utility[5] = beta_cons_quit

	-- for i = 1,7 do
	-- 	print("utility isg",i,": ", utility[i])
	-- end

end

--availability
--the logic to determine availability is the same with current implementation
local availability = {}
local function computeAvailabilities(params,dbparams)
	for i = 1, 5 do 
		availability[i] = dbparams:availability(i)
	end
end

--scale
local scale={}
scale["make"] = 4.82
scale["quit"] = 1

-- function to call from C++ preday simulator
-- params and dbparams tables contain data passed from C++
-- to check variable bindings in params or dbparams, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp
function choose_isg(params,dbparams)
	-- print("choose_isg: in")
	computeUtilities(params,dbparams) 
	-- print("choose_isg: computeUtilities")
	computeAvailabilities(params,dbparams)
	local probability = calculate_probability("nl", choice, utility, availability, scale)
	return make_final_choice(probability)
end

