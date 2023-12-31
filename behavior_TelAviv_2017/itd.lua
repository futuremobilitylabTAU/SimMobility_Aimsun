--[[
Model - intermediate stop time of day
Type - MNL
Authors - Siyu Li, Harish Loganathan
]]

-- all require statements do not work with C++. They need to be commented. The order in which lua files are loaded must be explicitly controlled in C++. 
--require "Logit"

--Estimated values for all betas
--Note= the betas that not estimated are fixed to zero.

local beta_dur_1_work = -0.993 * 10
local beta_dur_2_work = 0
local beta_dur_1_edu = -1.00 * 10
local beta_dur_2_edu = 0
local beta_dur_1_shop = -1.77 * 10
local beta_dur_2_shop = 0
local beta_dur_1_other = -1.5 * 10
local beta_dur_2_other = 0

local beta_arr_1_cos2pi = -4.29
local beta_arr_1_cos4pi = -1.79
local beta_arr_1_cos6pi = -0.335
local beta_arr_1_cos8pi = -0.0642
local beta_arr_1_sin2pi = 3.26
local beta_arr_1_sin4pi = -0.118
local beta_arr_1_sin6pi = 0.0340
local beta_arr_1_sin8pi = 0.237 

local beta_dep_1_cos2pi = 3.55
local beta_dep_1_cos4pi = -2.90
local beta_dep_1_cos6pi = -3.50
local beta_dep_1_cos8pi = -0.538
local beta_dep_1_sin2pi = 0.953
local beta_dep_1_sin4pi = 3.00
local beta_dep_1_sin6pi = -0.758
local beta_dep_1_sin8pi = -1.50

local beta_arr_tt = 0
local beta_dep_tt = 0
local beta_tt = -0.0437

local beta_cost = 0

local Begin={}	
local End={}
local choiceset={}
local arrmidpoint = {}
local depmidpoint = {}

for i =1,48 do
	Begin[i] = i
	End[i] = i
	arrmidpoint[i] = i * 0.5 + 2.75
	depmidpoint[i] = i * 0.5 + 2.75
end

for i = 1,48 do
	choiceset[i] = i
end

local utility = {}
local function computeUtilities(params,dbparams)
	local stoptype = dbparams.stop_type
	
	local work,edu,shop,other = 0,0,0,0
	
	if stoptype == 1 then
		work = 1
	elseif stoptype == 2 then
		edu = 1
	elseif stoptype == 3 then
		shop = 1	
	elseif stoptype == 4 then
		other = 1
	end

	local first_bound = dbparams.first_bound
	local second_bound = dbparams.second_bound 

	local high_tod = dbparams.high_tod
	local low_tod = dbparams.low_tod

	local pi = math.pi
	local sin = math.sin
	local cos = math.cos
	local pow = math.pow

	local function sarr_1(t)
		return beta_arr_1_sin2pi * sin(2*pi*t/24) + beta_arr_1_cos2pi * cos(2*pi*t/24) + beta_arr_1_sin4pi * sin(4*pi*t/24) + beta_arr_1_cos4pi * cos(4*pi*t/24) + beta_arr_1_sin6pi * sin(6*pi*t/24) + beta_arr_1_cos6pi * cos(6*pi*t/24) + beta_arr_1_sin8pi * sin(8*pi*t/24) + beta_arr_1_cos8pi * cos(8*pi*t/24)
	end

	local function sdep_1(t)
		return beta_dep_1_sin2pi * sin(2*pi*t/24) + beta_dep_1_cos2pi * cos(2*pi*t/24) + beta_dep_1_sin4pi * sin(4*pi*t/24) + beta_dep_1_cos4pi * cos(4*pi*t/24) + beta_dep_1_sin6pi * sin(6*pi*t/24) + beta_dep_1_cos6pi * cos(6*pi*t/24) + beta_dep_1_sin8pi * sin(8*pi*t/24) + beta_dep_1_cos8pi * cos(8*pi*t/24)
	end


	for i =1,48 do
		local arr = arrmidpoint[i]
		local dep = depmidpoint[i]
		local dur = first_bound*(high_tod-i+1)+second_bound*(i-low_tod+1)
		dur = 0.25 + (dur-1)/2
	
		utility[i] = sarr_1(arr) + sdep_1(dep) +
		dur * (work * beta_dur_1_work + edu * beta_dur_1_edu  + shop * beta_dur_1_shop + other * beta_dur_1_other) + 
		pow(dur,2) * (work * beta_dur_2_work + edu * beta_dur_2_edu + shop * beta_dur_2_shop + other * beta_dur_2_other) + beta_tt * dbparams:TT(i)

		-- print("utility ", i, ": ", utility[i])
	end

end

--availability
--the logic to determine availability is the same with current implementation
local availability = {}
local function computeAvailabilities(params,dbparams)
	for i = 1, 48 do 
		availability[i] = dbparams:availability(i)
	end
end

--scale
local scale= 1 -- for all choices

-- function to call from C++ preday simulator
-- params and dbparams tables contain data passed from C++
-- to check variable bindings in params or dbparams, refer PredayLuaModel::mapClasses() function in dev/Basic/medium/behavioral/lua/PredayLuaModel.cpp
function choose_itd(params,dbparams)
	computeUtilities(params,dbparams) 
	computeAvailabilities(params,dbparams)
	local probability = calculate_probability("mnl", choiceset, utility, availability, scale)
	
	prob = 0.0
	for i = 1,48 do
		prob = prob + probability[i]
	end
	--print("probability isg: ", prob)
	if prob < 0.001 then
		return -1
	else
		return make_final_choice(probability)
	end 

end

