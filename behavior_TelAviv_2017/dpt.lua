--[[
Model: Day Pattern Tours
Based on: dpb.lua (Siyu Li, Harish Loganathan)
Author: Isabel Viegas
Crated: January 28, 2017
Updated: August 16, 2017
]]

--grouping activities ->take maximum of the ones to be grouped
-- COEFFICIENTS
-- Tour Constants
local beta_tour_work = 0 -0.1 +0.05 +0.1 +0.01 -0.01 +0.01 +1.5 -1.5 +1.3 - 1.1 -0.124 + 0.5 -1 +1 -0.1 -0.2 -0.1 +0.1
local beta_tour_edu = -0.7 -0.8 +0.7 +0.1 +0.1 -0.1 +0.08
local beta_tour_shop = -3.7 + 0.2 -0.1 +0.08
local beta_tour_other = -3.6 -1 +0.6 +0.1 -0.1 +0.08

-- Person type
-- fulltime as a base
-- work as a base
local beta_parttime_work = 0  
local beta_parttime_edu = 1.68
local beta_parttime_shop = 0.720
local beta_parttime_other = 0.931

local beta_retired_work = 0
local beta_retired_edu = 0.577
local beta_retired_shop = 0.686
local beta_retired_other = 0.755

local beta_homemaker_work = 0
local beta_homemaker_edu = -0.0737
local beta_homemaker_shop = 0.823
local beta_homemaker_other = 1.29

local beta_unemployed_work = 1.14
local beta_unemployed_edu = 0.455
local beta_unemployed_shop = 0.643
local beta_unemployed_other = 1.09

local beta_student_work = 0
local beta_student_edu = 1.45
local beta_student_shop = 0.679
local beta_student_other = 0.873

local beta_preschool_work = 0
local beta_preschool_edu = 0
local beta_preschool_shop = 0
local beta_preschool_other = 0

local beta_studentK8_work = 0 
local beta_studentK8_edu = 1.03
local beta_studentK8_shop = -0.0876
local beta_studentK8_other = 0.618

local beta_student912_work = 0
local beta_student912_edu = 1.25
local beta_student912_shop = -0.0336
local beta_student912_other = 0.328

local beta_undergraduate_work = 0
local beta_undergraduate_edu = 0.644
local beta_undergraduate_shop = 0.0624
local beta_undergraduate_other = 0.176

local beta_graduate_work = 0
local beta_graduate_edu = 0.406
local beta_graduate_shop = 0.0591
local beta_graduate_other = 0.00508

local beta_otherstudent_work = 0
local beta_otherstudent_edu = 0
local beta_otherstudent_shop = 0
local beta_otherstudent_other = 0
-- Age Group
-- age 36-50 as a base
-- work as a base
local beta_age20_work = 0
local beta_age20_edu = 0.896
local beta_age20_shop = -0.390
local beta_age20_other = 0.454

local beta_age2025_work = 0
local beta_age2025_edu = 0.610
local beta_age2025_shop = -0.466
local beta_age2025_other = -0.0456

local beta_age2635_work = 0
local beta_age2635_edu = -0.706
local beta_age2635_shop = 0.0410
local beta_age2635_other = 0.153

local beta_age5165_work = 0
local beta_age5165_edu = -1.31
local beta_age5165_shop = 0.118
local beta_age5165_other = 0.163

local beta_age65_work = 0
local beta_age65_edu = -1.21
local beta_age65_shop = 0.130
local beta_age65_other = 0.364
-- Gender
-- male as a base
-- work as a base
local beta_female_work = 0
local beta_female_edu = -0.00779
local beta_female_shop = 0.262
local beta_female_other = 0.203
-- Income
local beta_INCOME_work = 0
local beta_INCOME_edu = 0.0155
local beta_INCOME_shop = 0.00208
local beta_INCOME_other = 0.0248

-- Transportation
local beta_LIC_work = 0
local beta_LIC_edu = -0.113
local beta_LIC_shop = 0.0842
local beta_LIC_other = 1.14

local beta_TRANS_work = 0
local beta_TRANS_edu = 0.123
local beta_TRANS_shop = -0.0653
local beta_TRANS_other = -0.0242

-- Additional Constants
-- onetour as a base
local beta_onetour = 0
local beta_twotour = -1.29-0.5-1 -1+1-0.4-0.3    -- -0.5-1-2.3
local beta_threetour = -5.34-1-1 -1+1-0.3      --  -2.3
 
-- Logsums 
local beta_logsumNU_work = 0.000996
local beta_logsumU_work = 0  --  -0.000285
local beta_logsum_edu =  0   --  -0.0343
local beta_logsum_shop = 0.0882
local beta_logsum_other = 0.101

-- Combination constants
local beta_workedu_tt = 0
local beta_workshop_tt = 1.55
local beta_workother_tt = 2.48
local beta_edushop_tt = 1.18
local beta_eduother_tt = 2.53
local beta_shopother_tt = 3.18

-- Choiceset 
local choice = {
        {1,0,0,0},
        {0,1,0,0},
        {0,0,1,0},
        {0,0,0,1},
        {1,1,0,0},
        {1,0,1,0},
        {1,0,0,1},
        {0,1,1,0},
        {0,1,0,1},
        {0,0,1,1},
        {1,1,0,1},
        {1,0,1,1},
        {1,1,1,0},
        {0,1,1,1}
}            

local WorkT = {1,0,0,0,1,1,1,0,0,0,1,1,1,0}
local EduT = {0,1,0,0,1,0,0,1,1,0,1,0,1,1}
local ShopT = {0,0,1,0,0,1,0,1,0,1,0,1,1,1}
local OtherT = {0,0,0,1,0,0,1,0,1,1,1,1,0,1}

  -- XXXtour_ . . series
local onetour = {1,1,1,1,0,0,0,0,0,0,0,0,0,0}
local twotour = {0,0,0,0,1,1,1,1,1,1,0,0,0,0}
local threetour = {0,0,0,0,0,0,0,0,0,0,1,1,1,1}

local workedu_tt = {0,0,0,0,1,0,0,0,0,0,1,0,1,0}
local workshop_tt = {0,0,0,0,0,1,0,0,0,0,0,1,1,0}
local workother_tt = {0,0,0,0,0,0,1,0,0,0,1,1,0,0}
local edushop_tt = {0,0,0,0,0,0,0,1,0,0,0,0,1,1}
local eduother_tt = {0,0,0,0,0,0,0,0,1,0,1,0,0,1}
local shopother_tt = {0,0,0,0,0,0,0,0,0,1,0,1,0,1}
local workshopother_tt = {0,0,0,0,0,0,0,0,0,0,0,1,0,0}

-- UTILITY
local utility = {}
local function computeUtilities(params) 
	local pid = params.person_id
	local person_type_id = params.person_type_id 
	local age_id = params.age_id
	local female_dummy = params.female_dummy
	local student_dummy = params.student_dummy
	local income_id = params.income_id -1
	--local income_mid = {3.40,3.85,4.38,4.93,5.46,6.09,6.67,7.16,8.16,9.60}
	local income_mid =  {0,0.67, 1.4, 2.07, 2.61, 3.05, 3.47, 3.91, 4.4, 5.04, 6.15}
	local missing_income = params.missing_income
	local license = params.has_driving_license --modified for MITei branch
	local studentTypeId = params.studentTypeId
	local transit = params.has_vanbus_license
	local fixedworktime = params.fixed_work_hour

	local usual = params.fixed_place

	local worklogsum = params:activity_logsum(1)
	local edulogsum = params:activity_logsum(2)
	local shoplogsum = params:activity_logsum(3)
	local otherlogsum = params:activity_logsum(4)
	
	-- Person type and student type related variables
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
	-- Age group related variables
	local age20,age2025,age2635,age3650,age5165,age65,missingage = 0,0,0,0,0,0,0
	if age_id < 4 then 
		age20 = 1
	elseif age_id == 5 then 
		age2025 = 1
	elseif age_id > 4 and age_id <= 5 then
		age2635 = 1
	elseif age_id > 5 and age_id <= 9 then
		age3650 = 1
	elseif age_id > 9 and age_id <= 12 then
		age5165 = 1
	elseif age_id > 12 then 
		age65 = 1
	end

	-- Income
	local INCOME = income_mid[income_id]

	-- Gender
	local female = 0
	if female_dummy == 0 then
		female = 1
	end

	-- License
	local LIC = 0
	if license == true then
		LIC = 1
	end

	-- Transit
	local TRANS = 0
	if transit == true then
		TRANS = 1
	end

	-- Work related
	local FLEXSCHED = 0
	if fixedworktime == false then
		FLEXSCHED = 1
	end

	local MULTJOBS = 0 
	
	--print('dpt: reached before utility calculation')	
	for i = 1,14 do
		utility[i] = beta_tour_work * (WorkT[i]) + 
	beta_tour_edu * (EduT[i]) +
        beta_tour_shop * (ShopT[i]) + 
	beta_tour_other * OtherT[i] +
        beta_parttime_work * (WorkT[i] * parttime) +  
        beta_parttime_edu * (EduT[i] * parttime) + 
        beta_parttime_shop * (ShopT[i] * parttime) + 
        beta_parttime_other * (OtherT[i] * parttime) +
        beta_retired_work * (WorkT[i] * retired) + 
        beta_retired_edu * (EduT[i] * retired) + 
        beta_retired_shop * (ShopT[i] * retired) + 
        beta_retired_other* (OtherT[i] * retired)  +
        beta_homemaker_work * (WorkT[i] * homemaker) + 
        beta_homemaker_edu * (EduT[i] * homemaker) + 
        beta_homemaker_shop * (ShopT[i] * homemaker) + 
        beta_homemaker_other* (OtherT[i] * homemaker)  +
        beta_unemployed_work * (WorkT[i] * unemployed) + 
        beta_unemployed_edu * (EduT[i] * unemployed) + 
        beta_unemployed_shop * (ShopT[i] * unemployed) + 
        beta_unemployed_other * (OtherT[i] * unemployed)  +
        beta_student_work * (WorkT[i] * student) + 
        beta_student_edu * (EduT[i] * student) + 
        beta_student_shop * (ShopT[i] * student) + 
        beta_student_other * (OtherT[i] * student)  +
        beta_preschool_work * (WorkT[i] * preschool) + 
        beta_preschool_edu * (EduT[i] * preschool) + 
        beta_preschool_shop * (ShopT[i] * preschool) + 
        beta_preschool_other * (OtherT[i] * preschool)  +
        beta_studentK8_work * (WorkT[i] * studentK8) + 
        beta_studentK8_edu * (EduT[i] * studentK8) + 
        beta_studentK8_shop * (ShopT[i] * studentK8) + 
        beta_studentK8_other * (OtherT[i] * studentK8)  +
        beta_student912_work * (WorkT[i] * student912) + 
        beta_student912_edu * (EduT[i] * student912) + 
        beta_student912_shop * (ShopT[i] * student912) + 
        beta_student912_other * (OtherT[i] * student912)  +
        beta_undergraduate_work * (WorkT[i] * undergraduate) + 
        beta_undergraduate_edu * (EduT[i] * undergraduate) + 
        beta_undergraduate_shop * (ShopT[i] * undergraduate) + 
        beta_undergraduate_other * (OtherT[i] * undergraduate)  +
	    beta_graduate_work * (WorkT[i] * graduate) + 
	    beta_graduate_edu * (EduT[i] * graduate) + 
	    beta_graduate_shop * (ShopT[i] * graduate) + 
	    beta_graduate_other * (OtherT[i] * graduate)  +
        beta_otherstudent_work * (WorkT[i] * otherstudent) + 
        beta_otherstudent_edu * (EduT[i] * otherstudent) + 
        beta_otherstudent_shop * (ShopT[i] * otherstudent) + 
        beta_otherstudent_other * (OtherT[i] * otherstudent)  +
        beta_age20_work * (WorkT[i] * age20) + beta_age20_edu * (EduT[i] * age20) + 
        beta_age20_shop * (ShopT[i] * age20) + beta_age20_other * (OtherT[i] * age20)  +
        beta_age2025_work * (WorkT[i] * age2025) + beta_age2025_edu * (EduT[i] * age2025) + 
        beta_age2025_shop * (ShopT[i] * age2025) + beta_age2025_other * (OtherT[i] * age2025)  +
        beta_age2635_work * (WorkT[i] * age2635) + beta_age2635_edu * (EduT[i] * age2635) + 
        beta_age2635_shop * (ShopT[i] * age2635) + beta_age2635_other* (OtherT[i] * age2635)  +
        beta_age5165_work * (WorkT[i] * age5165) + beta_age5165_edu * (EduT[i] * age5165) + 
        beta_age5165_shop * (ShopT[i] * age5165) + beta_age5165_other * (OtherT[i] * age5165)  +
        beta_age65_work * (WorkT[i] * age65) + beta_age65_edu * (EduT[i] * age65) + 
        beta_age65_shop * (ShopT[i] * age65) + beta_age65_other * (OtherT[i] * age65)  +
        beta_female_work * (WorkT[i] * female) + beta_female_edu * (EduT[i] * female) + 
        beta_female_shop * (ShopT[i] * female) + beta_female_other * (OtherT[i] * female)  +
        beta_INCOME_work * (WorkT[i] * INCOME) + beta_INCOME_edu * (EduT[i] * INCOME) + 
        beta_INCOME_shop * (ShopT[i] * INCOME) + beta_INCOME_other * (OtherT[i] * INCOME)  +
        beta_LIC_work * (WorkT[i] * LIC) + beta_LIC_edu * (EduT[i] * LIC) +
        beta_LIC_shop * (ShopT[i] * LIC) + beta_LIC_other * (OtherT[i] * LIC)  +
        beta_TRANS_work * (WorkT[i] * TRANS) + beta_TRANS_edu * (EduT[i] * TRANS) +
        beta_TRANS_shop * (ShopT[i] * TRANS) + beta_TRANS_other * (OtherT[i] * TRANS)  +
        beta_workedu_tt * (workedu_tt[i]) + 
        beta_workshop_tt * (workshop_tt[i]) + 
        beta_workother_tt * (workother_tt[i]) + 
        beta_edushop_tt * (edushop_tt[i]) + 
        beta_eduother_tt * (eduother_tt[i]) +
        beta_shopother_tt * (shopother_tt[i]) +
        beta_onetour * onetour[i] + beta_twotour * twotour[i] +
        beta_threetour * threetour[i] + 
        (beta_logsumU_work * usual * worklogsum + beta_logsumNU_work * (1-usual) * worklogsum) * (WorkT[i]) +
        beta_logsum_edu * edulogsum * EduT[i] + beta_logsum_shop * shoplogsum * ShopT[i] + 
        beta_logsum_other * otherlogsum * OtherT[i]
	end
end

--availability
local availability = {}
local function computeAvailabilities(params)
	-- storing data from params table passed into this function locally for use in this function (this is purely for better execution time)
	local student_dummy = params.student_dummy

	-- make education tour only available for students
	-- make work tour only available to workers and student
	for i = 1,14 do
		if student_dummy == 1 then
			availability[i] = 1
		else
			if choice[i][2] == 0 then 
				availability[i] = 1
			else
				availability[i] = 0
			end
		end
		if params.person_type_id > 2 and choice[i][1]==1 then
			availability[i] = 0
		end
	end
end

-- scales
local scale = 1 -- for all choices

-- function to call from C++ preday simulator
-- params table contains data passed from C++
-- to check variable bindings in params, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp
function choose_dpt(params)
	computeUtilities(params) 
	computeAvailabilities(params)
	local probability = calculate_probability("mnl", choice, utility, availability, scale)
	idx = make_final_choice(probability)
	return choice[idx]
end

-- function to call from C++ preday simulator for logsums computation
-- params table contain person data passed from C++
-- to check variable bindings in params, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp
function compute_logsum_dpt(params)

	computeUtilities(params,dbparams) 
	computeAvailabilities(params,dbparams)
	local probability = calculate_probability("mnl", choice, utility, availability, scale)
	local num_tours = 0
	for cno,prob in pairs(probability) do
		if cno <= 4 then
			num_tours = num_tours + prob
		elseif cno <= 10 then
			num_tours = num_tours + (2*prob)
		elseif cno <= 14 then
			num_tours = num_tours + (3*prob)
		end
	end
	local return_table = {}
	return_table[1] = compute_mnl_logsum(utility, availability)
	return_table[2] = 2 * num_tours --expected number of primary trips = 2*expected number of tours
	return return_table
end
