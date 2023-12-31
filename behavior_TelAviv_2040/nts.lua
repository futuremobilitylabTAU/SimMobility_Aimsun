--[[
Model: Number of Tours - Shop
Based on: dpb.lua (Siyu Li, Harish Loganathan)
Type: Binary Logit
Author: Isabel Viegas
Crated: November 21, 2016
Updated: July 12, 2017
]]

-- COEFFICIENTS
-- one shop tour as base
--local beta_cons_shop2 = -5.03+1+1+2.03-1+0.5-0.05-0.01-0.01            +0.5-0.1-0.5+0.2+0.1  +0.5-0.09-0.09  
local beta_cons_shop2 = -2.33 + 0.33 +0.1

-- Person type
-- fulltime as base
local beta_parttime_shop2 = 0.236
local beta_retired_shop2 = 0.195
local beta_homemaker_shop2 = 0.505
local beta_unemployed_shop2 = 0.398
local beta_student_shop2 = 0.550

-- Student Type
-- not a student as a base
local beta_preschool_shop2 = -0.951
local beta_studentK8_shop2 = -1.56
local beta_student912_shop2 = -2.72
local beta_undergraduate_shop2 = -0.700
local beta_graduate_shop2 = 0 -- not enough observations
local beta_otherstudent_shop2 = -0.493

-- Age group
-- adge 36 to 50 as base
-- one shop tour as base
-- all gategories turned out to be very insignificant
local beta_age20_shop2 = 0
local beta_age2025_shop2 = 0
local beta_age2635_shop2 = 0
local beta_age5165_shop2 = 0 
local beta_age65_shop2 = 0 

-- Gender
-- male as base
local beta_female_shop2 = -0.183

--Personal income
local beta_INCOME_shop2 = 0

--Others
local beta_LIC_shop2 = 0
local beta_TRANS_shop2 = 0

local beta_logsum_shop2 = 0.0225



--choiceset
local choice = {
		1,
		2
}


-- UTILITY
local utility = {}
local function computeUtilities(params) 
	local pid = params.person_id
	local person_type_id = params.person_type_id 
	local age_id = params.age_id
	local female_dummy = params.female_dummy
	local income_id = params.income_id -1
	-- local income_mid =  {3.40,3.85,4.38,4.93,5.46,6.09,6.67,7.16,8.16,9.60}
	local income_mid =  {0,0.67, 1.4, 2.07, 2.61, 3.05, 3.47, 3.91, 4.4, 5.04, 6.15}
	local missing_income = params.missing_income
	local license = params.has_car_license
	local transit = params.has_vanbus_license
	local fixedshoptime = params.fixed_shop_hour
	local usual = params.fixed_place

	local studentTypeId = params.studentTypeId
	local student_dummy = params.student_dummy
	
	local shoplogsum = params:activity_logsum(3)

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
	student = studentTypeId ==0 and 0 or 1
	-- Age group
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
	local LIC = 0
	if license == true then
		LIC = 1
	end

	local TRANS = 0
	if transit == true then
		TRANS = 1
	end

	
	utility[1] = 0
	utility[2] = beta_cons_shop2 + beta_parttime_shop2 * parttime +
	beta_retired_shop2 * retired + beta_homemaker_shop2 * homemaker +
	beta_unemployed_shop2 * unemployed + beta_student_shop2 * student +
	beta_preschool_shop2 * preschool + beta_studentK8_shop2 * studentK8 +
	beta_student912_shop2 * student912 + beta_undergraduate_shop2 * undergraduate +
	beta_graduate_shop2 * graduate + beta_otherstudent_shop2 * otherstudent +
   	beta_age20_shop2 * age20  + beta_age2025_shop2 * age2025 + beta_age65_shop2 * age65 +
    beta_age2635_shop2 * age2635 + beta_age5165_shop2 * age5165 +
    beta_INCOME_shop2 * INCOME + beta_female_shop2 * female +
    beta_LIC_shop2 * LIC + beta_TRANS_shop2 * TRANS +
    beta_logsum_shop2 *  shoplogsum

end

-- availability
local availability = {1,1}


-- scales
local scale = 1 --for all choices

-- function to call from C++ preday simulator
-- params table contains data passed from C++
-- to check variable bindings in params, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp
function choose_nts(params)
	computeUtilities(params) 
	local probability = calculate_probability("mnl", choice, utility, availability, scale)
	return make_final_choice(probability)
end



