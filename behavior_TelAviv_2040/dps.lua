--[[
Model: Day Pattern Stops
Based on: dpb.lua (Siyu Li, Harish Loganathan)
Author: Isabel Viegas
Crated: January 22, 2017
Updated: July 20, 2017
]]

-- COEFFICIENTS
-- Tour Constants
local beta_stop_work = -2.6 -0.1 +0.3 -0.1 -0.1 -0.1
local beta_stop_edu = -10.2 -0.2 -0.5 +0.2 +0.4	+0.4 -0.2 +1 -0.3 -0.2 -0.2 +0.1
local beta_stop_shop = 6.7 -0.5 +1 +0.2 -1 +0.1 +0.1 -0.1
local beta_stop_other = -1.4 +0.2 -0.5 +0.2 +0.2

-- Person type
-- fulltime as a base
-- work as a base
local beta_parttime_work = 0
local beta_parttime_edu = 0.454
local beta_parttime_shop = 0.382
local beta_parttime_other = 0.194

local beta_retired_work = 0
local beta_retired_edu = 0.689
local beta_retired_shop = 0.845
local beta_retired_other = 0.396

local beta_homemaker_work = 0
local beta_homemaker_edu = 0
local beta_homemaker_shop = 0.893
local beta_homemaker_other = 0.395

local beta_unemployed_work = 0
local beta_unemployed_edu = 0
local beta_unemployed_shop = 0.698
local beta_unemployed_other = 0.583

local beta_preschool_work = 0
local beta_preschool_edu = 3.24
local beta_preschool_shop = 0
local beta_preschool_other = 0.78

local beta_studentK8_work = 0 
local beta_studentK8_edu = 2.84
local beta_studentK8_shop = 0
local beta_studentK8_other = 0.897

local beta_student912_work = 0
local beta_student912_edu = 3.10
local beta_student912_shop = -0.511
local beta_student912_other = 0

local beta_undergraduate_work = 0
local beta_undergraduate_edu = 3.10
local beta_undergraduate_shop = 0
local beta_undergraduate_other = 0

local beta_graduate_work = 0
local beta_graduate_edu = 0
local beta_graduate_shop = 0
local beta_graduate_other = 0 

local beta_otherstudent_work = 0
local beta_otherstudent_edu = 0
local beta_otherstudent_shop = 0
local beta_otherstudent_other = 0
-- Age group
-- under 20 and over 65 is a base
-- Work as a base

local beta_age20_work = 0
local beta_age20_edu = 0.964
local beta_age20_shop = -0.314
local beta_age20_other = 0.231

local beta_age2025_work = 0
local beta_age2025_edu = 1.40
local beta_age2025_shop = -0.235
local beta_age2025_other = 0.306

local beta_age2635_work = 0
local beta_age2635_edu = 1.40
local beta_age2635_shop = -0.202
local beta_age2635_other = 0

local beta_age5165_work = 0
local beta_age5165_edu = 0
local beta_age5165_shop = 0.227
local beta_age5165_other = 0.135

local beta_age65_work = 0
local beta_age65_edu = 0
local beta_age65_shop = 0
local beta_age65_other = 0

-- Gender
-- male as a base
-- work as a base
local beta_female_work = 0
local beta_female_edu = 0
local beta_female_shop = 0.252 
local beta_female_other = 0.198
-- Income
local beta_INCOME_work = 0
local beta_INCOME_edu = -0.0124
local beta_INCOME_shop = 0
local beta_INCOME_other = 0.0271

local beta_LIC_work = 0
local beta_LIC_edu = -0.631
local beta_LIC_shop = 0
local beta_LIC_other = 0.956

local beta_TRANS_work = 0
local beta_TRANS_edu = 0
local beta_TRANS_shop = 0
local beta_TRANS_other = 0
-- Additional constants
-- onestop as base
local beta_onestop = 0                       
local beta_twostops = 1.91    
local beta_threestops = 0

-- Combination constants
local beta_workedu_ss = 0
local beta_workshop_ss = 1.01
local beta_workother_ss = 2.54
local beta_edushop_ss = 0.816
local beta_eduother_ss = 3.48
local beta_shopother_ss = 1.60

-- choiceset 
local choice = {
        {0,0,0,0},
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
	{1,1,1,0},
	{1,1,0,1},
	{1,0,1,1},
	{0,1,1,1}
}          

-- Inclusion of purpose in tour option

local WorkI =  {0,1,0,0,0,1,1,1,0,0,0,1,1,1,0}
local EduI =   {0,0,1,0,0,1,0,0,1,1,0,1,1,0,1}
local ShopI =  {0,0,0,1,0,0,1,0,1,0,1,1,0,1,1}
local OtherI = {0,0,0,0,1,0,0,1,0,1,1,0,1,1,1}

-- Number of tours
local onestop =  {0,1,1,1,1,0,0,0,0,0,0,0,0,0,0}
local twostop =  {0,0,0,0,0,1,1,1,1,1,1,0,0,0,0}
local threestop ={0,0,0,0,0,0,0,0,0,0,0,1,1,1,1}
-- Tour interactions 
local workedu_ss =   {0,0,0,0,0,1,0,0,0,0,0,1,1,0,0}
local workshop_ss =  {0,0,0,0,0,0,1,0,0,0,0,1,0,1,0}
local workother_ss = {0,0,0,0,0,0,0,1,0,0,0,0,1,1,0}
local edushop_ss =   {0,0,0,0,0,0,0,0,1,0,0,1,0,0,1}
local eduother_ss =  {0,0,0,0,0,0,0,0,0,1,0,0,1,0,1}
local shopother_ss = {0,0,0,0,0,0,0,0,0,0,1,0,0,1,1}
-- UTILITY
local utility = {}

local function computeUtilities(params)
	local person_type_id = params.person_type_id 
	local age_id = params.age_id
	local female_dummy = params.female_dummy
	local student_dummy = params.student_dummy
	local income_id = params.income_id -1
	--local income_mid = {3.40,3.85,4.38,4.93,5.46,6.09,6.67,7.16,8.16,9.60}
	local income_mid =  {0,0.67, 1.4, 2.07, 2.61, 3.05, 3.47, 3.91, 4.4, 5.04, 6.15}
	local missing_income = params.missing_income
	local license = params.has_driving_license
	local studentTypeId = params.studentTypeId
	local transit = params.has_vanbus_license
	local fixedworktime = params.fixed_work_hour
	
	-- Person type and student type 
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
	student = studentTypeId ==0 and 0 or 1	-- Age group
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

	-- Gender
	local female = 0
	if female_dummy == 0 then
		female = 1
	end
	
	-- Income
	local INCOME = income_mid[income_id]

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
		
	for i = 1,15 do
		utility[i] = beta_stop_work * (WorkI[i]) + beta_stop_edu * (EduI[i]) +
        	beta_stop_shop * (ShopI[i]) + beta_stop_other * (OtherI[i]) +
        	beta_parttime_work * (WorkI[i] * parttime) +  beta_parttime_edu * (EduI[i] * parttime) + 
        	beta_parttime_shop * (ShopI[i] * parttime) + beta_parttime_other * (OtherI[i] * parttime) +
        	beta_retired_work * (WorkI[i] * retired) + beta_retired_edu * (EduI[i] * retired) + 
        	beta_retired_shop * (ShopI[i] * retired) + beta_retired_other * (OtherI[i] * retired)  +
	        beta_homemaker_work * (WorkI[i] * homemaker) + beta_homemaker_edu * (EduI[i] * homemaker) + 
	        beta_homemaker_shop * (ShopI[i] * homemaker) + beta_homemaker_other * (OtherI[i] * homemaker)  +
	        beta_unemployed_work * (WorkI[i] * unemployed) + beta_unemployed_edu * (EduI[i] * unemployed) + 
	        beta_unemployed_shop * (ShopI[i] * unemployed) + beta_unemployed_other * (OtherI[i] * unemployed) +
	        beta_preschool_work * (WorkI[i] * preschool) + beta_preschool_edu * (EduI[i] * preschool) + 
	        beta_preschool_shop * (ShopI[i] * preschool) + beta_preschool_other * (OtherI[i] * preschool)  +
	        beta_studentK8_work * (WorkI[i] * studentK8) + beta_studentK8_edu * (EduI[i] * studentK8) + 
	        beta_studentK8_shop * (ShopI[i] * studentK8) + beta_studentK8_other * (OtherI[i] * studentK8)  +
	        beta_student912_work * (WorkI[i] * student912) + beta_student912_edu * (EduI[i] * student912) + 
	        beta_student912_shop * (ShopI[i] * student912) + beta_student912_other* (OtherI[i] * student912)  +
	        beta_undergraduate_work * (WorkI[i] * undergraduate) + beta_undergraduate_edu * (EduI[i] * undergraduate) + 
	        beta_undergraduate_shop * (ShopI[i] * undergraduate) + beta_undergraduate_other * (OtherI[i] * undergraduate)  +
	        beta_graduate_work * (WorkI[i] * graduate) + beta_graduate_edu * (EduI[i] * graduate) + 
	        beta_graduate_shop * (ShopI[i] * graduate) + beta_graduate_other * (OtherI[i] * graduate)  +
	        beta_otherstudent_work * (WorkI[i] * otherstudent) + beta_otherstudent_edu * (EduI[i] * otherstudent) + 
	        beta_otherstudent_shop * (ShopI[i] * otherstudent) + beta_otherstudent_other * (OtherI[i] * otherstudent) +
	        beta_age20_work * (WorkI[i] * age20) + beta_age20_edu * (EduI[i] * age20) + 
	        beta_age20_shop * (ShopI[i] * age20) + beta_age20_other * (OtherI[i] * age20)  +
	        beta_age2025_work * (WorkI[i] * age2025) + beta_age2025_edu * (EduI[i] * age2025) + 
	        beta_age2025_shop * (ShopI[i] * age2025) + beta_age2025_other * (OtherI[i] * age2025)  +
	        beta_age2635_work * (WorkI[i] * age2635) + beta_age2635_edu * (EduI[i] * age2635) + 
	        beta_age2635_shop * (ShopI[i] * age2635) + beta_age2635_other * (OtherI[i] * age2635)  +
	        beta_age5165_work * (WorkI[i] * age5165) + beta_age5165_edu * (EduI[i] * age5165) + 
	        beta_age5165_shop * (ShopI[i] * age5165) + beta_age5165_other * (OtherI[i] * age5165)  +
	        beta_age65_work * (WorkI[i] * age65) + beta_age65_edu * (EduI[i] * age65) + 
	        beta_age65_shop * (ShopI[i] * age65) + beta_age65_other * (OtherI[i] * age65) +
	        beta_female_work * (WorkI[i] * female) + beta_female_edu * (EduI[i] * female) + 
	        beta_female_shop * (ShopI[i] * female) + beta_female_other * (OtherI[i] * female)  +
	        beta_INCOME_work * (WorkI[i] * INCOME) + beta_INCOME_edu * (EduI[i] * INCOME) +
	        beta_INCOME_shop * (ShopI[i] * INCOME) + beta_INCOME_other * (OtherI[i] * INCOME) +
	        beta_workedu_ss * workedu_ss[i] + 
	        beta_workshop_ss * workshop_ss[i] + beta_workother_ss * workother_ss[i] +
	        beta_edushop_ss * edushop_ss[i] + beta_eduother_ss * eduother_ss[i] +
	        beta_shopother_ss * shopother_ss[i] +
	        beta_onestop * onestop[i] + beta_twostops * twostop[i] 
	end


end

--availability
local availability = {}
local function computeAvailabilities(params)
        local student_dummy = params.student_dummy

        -- make education tour only available for students
        -- make work tour only available to workers and student
        for i = 1,15 do
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
function choose_dps(params)
	computeUtilities(params) 
	computeAvailabilities(params)
	local probability = calculate_probability("mnl", choice, utility, availability, scale)
	idx = make_final_choice(probability)
	return choice[idx]
end

-- function to call from C++ preday simulator for logsums computation
-- params table contain person data passed from C++
-- to check variable bindings in params, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp
function compute_logsum_dps(params)
	computeUtilities(params) 
	computeAvailabilities(params)
	return compute_mnl_logsum(utility, availability)
end
