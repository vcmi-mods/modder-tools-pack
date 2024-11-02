#How to run this script?
# Via command prompt:
#	1. Open command prompt and set working directory same as path to this script
#	2. Type name of this script
#	3. Drag and drop valid JSON file
#	You also can specify many files by repeating step 3. but remember to separate them by space
# Via dropping files and folders with JSONs over script icon 

#Program author: Macron 1
#Original formulas of AI/Fight Value are given by
#GrayFace (http://wforum.heroes35.net/)

#Ported to Python by Kantor

import os
import sys
import math

BalancedJSONsFolderName = ['BALANCED_JSONs']

JSONfields = [
    '"max"',          # 0
    '"min"',          # 1
    '"val"',          # 2
    '"level"',        # 3
    '"attack"',       # 4
    '"defense"',      # 5
    '"hitPoints"',    # 6
    '"damage"',       # 7
    '"speed"',        # 8
    '"upgrades"',     # 9
    '"advMapAmount"', # 10
    '"aiValue"',      # 11
    '"fightValue"'    # 12
]

#Each value represents attack of unupgraded and upgraded creature, for example;
#first two values are 4 and 6, 4 is attack of pikeman and 6 is of halberdier,
#second two values belong to archer and marksman, and so on
stdAttack = [
4,6,6,6,8,9,10,12,12,12,15,16,20,30,5,6,6,7,9,9,9,9,9,9,15,15,18,
27,3,4,6,7,7,9,11,12,12,12,16,16,19,24,2,4,6,7,10,10,10,10,13,13,
16,16,19,26,5,6,5,5,7,7,10,10,13,13,16,18,17,19,4,5,6,6,9,10,9,10,
14,15,15,16,19,25,4,5,7,8,8,8,13,13,13,13,15,17,17,19,3,4,5,6,10,
11,7,8,11,12,14,14,16,18,9,10,10,8,11,13,2,2,15,15,0,8,0,11,0,9,0,
12,18,21,50,40,20,30,17,12,4,1,6,7,9,8,14,10,10,0,0,10,40,36,32,
35,25,33,25,25,28
]

stdDefence = [
5,5,3,3,8,9,12,12,7,10,15,16,20,30,3,3,7,7,5,5,8,10,12,12,14,14,18,27,
3,4,6,7,10,10,8,9,12,12,13,13,16,24,3,4,4,4,6,8,10,10,13,13,12,14,21,28,
4,6,5,5,7,7,9,10,10,10,16,18,15,17,3,4,5,6,7,8,9,10,12,15,13,14,19,25,
2,3,5,5,4,4,7,7,11,11,12,13,17,19,5,6,6,8,14,16,9,10,11,12,14,14,18,20,
9,10,8,10,12,12,2,2,13,13,0,10,0,11,0,9,0,8,18,18,50,40,20,30,12,10,2,
1,5,7,8,3,7,10,10,0,5,5,40,36,32,37,23,33,25,27,28
]

#  1 - name of ability to search (percents)
#  2 - bonus to fight value (percents)
#  3 - bonus to ai value (percents)
#  4 - bonus to damage (percents) not used now
#  5 - reserved
#  6 - reserved
Abilities = [
  [ 'NON_LIVING',      2, 2, 0, 0, 0 ],
  [ 'UNDEAD',          2, 2, 0, 0, 0 ],
  [ 'DRAGON_NATURE',   1, 1, 0, 0, 0 ],
  [ 'KING1',           1, 1, 0, 0, 0 ],
  [ 'KING2',           2, 2, 0, 0, 0 ],
  [ 'KING3',           3, 3, 0, 0, 0 ],
  [ 'FEARLESS',        5, 5, 0, 0, 0 ],
  [ 'NO_LUCK',         1, 1, 0, 0, 0 ],
  [ 'NO_MORALE',       1, 1, 0, 0, 0 ],
  [ 'SELF_MORALE',     2, 2, 0, 0, 0 ],
  [ 'SELF_LUCK',       2, 2, 0, 0, 0 ],
  [ 'FLYING',                    7, 7, 0, 0, 0 ],
  [ 'SHOOTER',                   10, 10, 0, 0, 0 ],
  [ 'CHARGE_IMMUNITY',           2, 2, 0, 0, 0 ],
  [ 'ADDITIONAL_ATTACK',         0, 0, 0, 0, 0 ],
  [ 'UNLIMITED_RETALIATIONS',    10, 10, 0, 0, 0 ],
  [ 'ADDITIONAL_RETALIATION',    5, 5, 0, 0, 0 ],
  [ 'JOUSTING',                  3, 3, 0, 0, 0 ],
  [ 'HATE',                      1, 1, 0, 0, 0 ],
  [ 'SPELL_LIKE_ATTACK',         3, 3, 0, 0, 0 ],
  [ 'THREE_HEADED_ATTACK',       0, 0, 0, 0, 0 ],
  [ 'ATTACKS_ALL_ADJACENT',      0, 0, 0, 0, 0 ],
  [ 'TWO_HEX_ATTACK_BREATH',     0, 0, 0, 0, 0 ],
  [ 'RETURN_AFTER_STRIKE',       3, 3, 0, 0, 0 ],
  [ 'ENEMY_DEFENCE_REDUCTION',   0, 0, 0, 0, 0 ],
  [ 'GENERAL_DAMAGE_REDUCTION',  5, 5, 0, 0, 0 ],
  [ 'GENERAL_ATTACK_REDUCTION',  0, 0, 0, 0, 0 ],
  [ 'DEFENSIVE_STANCE',          5, 5, 0, 0, 0 ],
  [ 'NO_DISTANCE_PENALTY',       7, 7, 0, 0, 0 ],
  [ 'NO_MELEE_PENALTY',          5, 5, 0, 0, 0 ],
  [ 'NO_WALL_PENALTY',           3, 3, 0, 0, 0 ],
  [ 'FREE_SHOOTING',             10, 10, 0, 0, 0 ],
  [ 'BLOCKS_RETALIATION',        5, 5, 0, 0, 0 ],
  [ 'CATAPULT',                     10, 10, 0, 0, 0 ],
  [ 'CHANGES_SPELL_COST_FOR_ALLY',  7, 7, 0, 0, 0 ],
  [ 'CHANGES_SPELL_COST_FOR_ENEMY', 7, 7, 0, 0, 0 ],
  [ 'SPELL_RESISTANCE_AURA',        5, 5, 0, 0, 0 ],
  [ 'HP_REGENERATION',              2, 2, 0, 0, 0 ],
  [ 'FULL_HP_REGENERATION',         3, 3, 0, 0, 0 ],
  [ 'MANA_DRAIN',                   3, 3, 0, 0, 0 ],
  [ 'MANA_CHANNELING',              3, 3, 0, 0, 0 ],
  [ 'LIFE_DRAIN',                   5, 5, 0, 0, 0 ],
  [ 'DOUBLE_DAMAGE_CHANCE',         0, 0, 0, 0, 0 ],
  [ 'FEAR',                         10, 10, 0, 0, 0 ],
  [ 'HEALER',                       3, 3, 0, 0, 0 ],
  [ 'FIRE_SHIELD',                  7, 7, 0, 0, 0 ],
  [ 'MAGIC_MIRROR',                 4, 4, 0, 0, 0 ],
  [ 'ACID_BREATH',                  3, 3, 0, 0, 0 ],
  [ 'DEATH_STARE',                  10, 10, 0, 0, 0 ],
  [ 'SPELLCASTER',            5, 5, 0, 0, 0 ],
  [ 'ENCHANTER',              10, 10, 0, 0, 0 ],
  [ 'RANDOM_SPELLCASTER',     4, 4, 0, 0, 0 ],
  [ 'SPELL_AFTER_ATTACK',     3, 3, 0, 0, 0 ],
  [ 'SPELL_BEFORE_ATTACK',    3, 3, 0, 0, 0 ],
  [ 'CASTS',                  0, 0, 0, 0, 0 ],
  [ 'SPECIFIC_SPELL_POWER',   0, 0, 0, 0, 0 ],
  [ 'CREATURE_SPELL_POWER',   0, 0, 0, 0, 0 ],
  [ 'CREATURE_ENCHANT_POWER', 0, 0, 0, 0, 0 ],
  [ 'DAEMON_SUMMONING',       7, 7, 0, 0, 0 ],
  [ 'REBIRTH',                5, 5, 0, 0, 0 ],
  [ 'ENCHANTED',              5, 5, 0, 0, 0 ],
  [ 'LEVEL_SPELL_IMMUNITY',   10, 10, 0, 0, 0 ],
  [ 'MAGIC_RESISTANCE',       5, 5, 0, 0, 0 ],
  [ 'SPELL_DAMAGE_REDUCTION', 2, 2, 0, 0, 0 ],
  [ 'MORE_DAMAGE_FROM_SPELL', -2, -2, 0, 0, 0 ],
  [ 'WATER_IMMUNITY',         2, 2, 0, 0, 0 ],
  [ 'EARTH_IMMUNITY',         2, 2, 0, 0, 0 ],
  [ 'AIR_IMMUNITY',           2, 2, 0, 0, 0 ],
  [ 'MIND_IMMUNITY',          2, 2, 0, 0, 0 ],
  [ 'SPELL_IMMUNITY',         1, 1, 0, 0, 0 ],
  [ 'DIRECT_DAMAGE_IMMUNITY', 10, 10, 0, 0, 0 ],
  [ 'RECEPTIVE',              3, 3, 0, 0, 0 ],
  [ 'POISON',                   3, 3, 0, 0, 0 ],
  [ 'SLAYER',                   3, 3, 0, 0, 0 ],
  [ 'BIND_EFFECT',              0, 0, 0, 0, 0 ],
  [ 'FORGETFULL',               -7, -7, 0, 0, 0 ],
  [ 'NOT_ACTIVE',               -10, -10, 0, 0, 0 ],
  [ 'ALWAYS_MINIMUM_DAMAGE',    -5, -5, 0, 0, 0 ],
  [ 'ALWAYS_MAXIMUM_DAMAGE',    7, 7, 0, 0, 0 ],
  [ 'ATTACKS_NEAREST_CREATURE', -5, -5, 0, 0, 0 ],
  [ 'IN_FRENZY',                2, 2, 0, 0, 0 ],
  [ 'HYPNOTIZED',               -10, -10, 0, 0, 0 ]
]

def readSpecifiedFile(FileName):
	file = open(FileName, 'r')
	content = [text.strip('\n') for text in file.readlines()]
	file.close()
	
	return content

def calcDamageCoeff(Attack, Defence):
	AvgSkill = 4
	A = Attack + AvgSkill
	D = Defence + AvgSkill
	
	if A >= D :
		return int(round(1.0 + min( (A - D) * 0.05, 3.0) ))
	else:
		return int(round(1.0 - min( (D - A) * 0.025, 0.7) ))

def calcAttDamage(Attack, EnemyDefenceReduction):
	Result = 0.0
	for i in stdDefence:
		Result += calcDamageCoeff(Attack, i * (1 - EnemyDefenceReduction) )
		
	Result /= 159
	return int(round(Result))
	
def calcDefDamage(Defence, GeneralAttackReduction):
	Result = 0.0
	for i in stdAttack:
		Result += calcDamageCoeff(i * (1 - GeneralAttackReduction), Defence)
		
	Result /= 159
	return int(round(Result))

def calcFinal(AttV, DefV, ProtPower, Mul):
	if AttV == 0 :
		return 0
	else:
		return int(round(math.sqrt(AttV) * pow(DefV, ProtPower) * Mul))

def calculateValues(Attack, Defence, HitPoints, MinDamage, MaxDamage,
                    GeneralAttackReduction, EnemyDefenceReduction):
	DmgFactor = 0.5
	ProtPowerFight = 0.57 # Less for Fight value
	ProtPowerAI = 0.67 # More for AI value
	MulFight = 1
	MulAI = 0.6
	
	AttV = calcAttDamage(Attack, EnemyDefenceReduction) *   \
            (DmgFactor * MaxDamage + (1 - DmgFactor) * MinDamage) * 50 + 1
	DefV = (7 / calcDefDamage(Defence, GeneralAttackReduction) + 1) * HitPoints + 1
	
	FinalV = calcFinal(AttV, DefV, ProtPowerFight, MulFight)
	FinalAI = calcFinal(AttV, DefV, ProtPowerAI, MulAI)
	
	return [int(FinalV), int(FinalAI)]

#Works for fields containing integers only
def ExtractValue(Line, FieldName):
	if Line.count(',') > 0 :
		if Line.find(',') < Line.find(FieldName) :
			Line = Line[Line.find(',') + 1:]
		else :
			Line = Line[:Line.find(',')]
	if Line.find('{') != -1 : Line = Line[Line.find('{') + 1 :]
	if Line.find('}') != -1 : Line = Line[:Line.find('}')]
	if Line.find('//') != -1 : Line = Line[:Line.find('//')]
	Line = Line[Line.find(':') + 1:].strip()
	return int(Line)

# Returns True if given line contains specified text and
# text isn't commented out, false otherwise
def isNotCommentedOut(Line, Text): 
	textPos = Line.find(Text)
	if textPos == -1 :
		return False
	commentPos = Line.find('//')
	if commentPos == -1 :
		return True
	elif commentPos < textPos :
		return False
	return True


def GetValueFromList(FileContent, SeekedString):
	braces = 0
	for line in FileContent:
		braces += line.count('{')
		braces -= line.count('}')
		
		if isNotCommentedOut(line, SeekedString) == True :
			if line.count('"') > 2 :
				continue # eg. "attack" : "something.wav"
			if braces < 3:
				textLine = line
				break
	return ExtractValue(textLine, SeekedString)

def GetBooleanAbilityExistence(FileContent, SeekedString):
	for line in FileContent:
		if isNotCommentedOut(line, SeekedString) == True:
			return True
	return False

def GetMaxMinFromList(FileContent, PropertyName):
	Min = Max = -1
	found = False
	for line in FileContent:
		if isNotCommentedOut(line, PropertyName) == True :
			found = True
		if found == True :
			if isNotCommentedOut(line, JSONfields[0]) == True :
				Max = ExtractValue(line, JSONfields[0])
			if isNotCommentedOut(line, JSONfields[1]) == True : 
				Min = ExtractValue(line, JSONfields[1])
			if line.count('}') > 0 :
				found = False
	return [Max, Min]

# Replaces value which must be formatted like "VALUE_NAME" : 0,
# and not like "VALUE_NAME" : 0, "VALUE_NAME" : 0
def ReplaceValue(FileContent, SearchValue, WriteValue):
	braces = 0;

	for Line in range(len(FileContent)):
		braces += FileContent[Line].count('{')
		braces -= FileContent[Line].count('}')
		
		if isNotCommentedOut(FileContent[Line], SearchValue) == False :
			continue
		else:
			if braces  < 3 :
				commentContent = ''
				if FileContent[Line].find('//') != -1 : #kopiujemy zawartosc komentarza
					commentContent = FileContent[Line][FileContent[Line].find('//'):]
				semicolonPos = FileContent[Line].find(':')
				hasColon = FileContent[Line].count(',')
				hasSpaceAfterSemicolon = FileContent[Line][semicolonPos + 1:].count(' ') #kosmetyka
				
				FileContent[Line] = FileContent[Line][:semicolonPos + 1]
				if hasSpaceAfterSemicolon : FileContent[Line] += ' '
				FileContent[Line] += str(WriteValue) #dopisujemy zamieniona wartosc
				if hasColon : FileContent[Line] += ','
				FileContent[Line] += commentContent

# Replaces two values "max" and "min" within specified property
def ReplaceValueMinMax(FileContent, SearchValue, WriteMin, WriteMax):
	found = False 
	for Line in range(len(FileContent)):		
		if isNotCommentedOut(FileContent[Line], SearchValue):
			found = True		
		if found == True:
			if isNotCommentedOut(FileContent[Line], JSONfields[0]) == True:
				FileContent[Line] = FileContent[Line].replace(' ', '') # get rid of spaces
				strOldMax = str( GetMaxMinFromList(FileContent, SearchValue)[0] )
				strMaxToReplace = '"max":' + strOldMax
				FileContent[Line] = FileContent[Line].replace( \
                        strMaxToReplace, ' "max":' + str(WriteMax))
				FileContent[Line] = FileContent[Line].replace(':', ' : ')			
			if isNotCommentedOut(FileContent[Line], JSONfields[1]) == True:
				FileContent[Line] = FileContent[Line].replace(' ', '') # get rid of spaces
				strOldMin = str( GetMaxMinFromList(FileContent, SearchValue)[1] )
				strMinToReplace = '"min":' + strOldMin
				FileContent[Line] = FileContent[Line].replace( \
                        strMinToReplace, ' "min":' + str(WriteMin))
				FileContent[Line] = FileContent[Line].replace(':', ' : ')
			if FileContent[Line].count('}') :
				found = False
				break

def BalanceProcedure(FileContent, Params):
	def CorrectValueWithinRange(Value, Min, Max):
		if Value > Max   : return Max
		elif Value < Min : return Min
		else : return Value
		
#1 - attack
#2 - defense
#3 - hit points
#4 - damage min
#5 - damage max
#6 - level of creature
	AttackSkill =  Params[0]
	DefenceSkill = Params[1]
	HitPoints =    Params[2]
	MaxDamage =    Params[3]
	MinDamage =    Params[4]
	Level =        Params[5]
	
	if 0 >= Level > 7 :
		return Params
	else:
		if AttackSkill  < 0 : AttackSkill  = 0
		if DefenceSkill < 0 : DefenceSkill = 0
		if MinDamage    < 0 : MinDamage    = 0
		if MaxDamage    < 0 : MaxDamage    = 0
		if HitPoints    < 0 : HitPoints    = 1
		
		if Level == 1 :
			if AttackSkill >  7 : AttackSkill =  7
			if DefenceSkill > 7 : DefenceSkill = 7
			if MaxDamage >    4 : MaxDamage =    4
			if MinDamage > MaxDamage : MinDamage = MaxDamage - 1
			if HitPoints > 11 : HitPoints = 11;
		if Level == 2 :
			AttackSkill =  CorrectValueWithinRange(AttackSkill,  4, 10)
			DefenceSkill = CorrectValueWithinRange(DefenceSkill, 2, 7)
			MaxDamage =    CorrectValueWithinRange(MaxDamage,    2, 5)
			HitPoints =    CorrectValueWithinRange(HitPoints,    9, 16)
			if MinDamage < 2 : MinDamage = min(2, MaxDamage)
			if MinDamage > MaxDamage : MinDamage = MaxDamage - 1
		if Level == 3 :   
			AttackSkill =  CorrectValueWithinRange(AttackSkill,  6, 11)
			DefenceSkill = CorrectValueWithinRange(DefenceSkill, 3, 11)
			MaxDamage =    CorrectValueWithinRange(MaxDamage,    1, 8)
			HitPoints =    CorrectValueWithinRange(HitPoints,   16, 38)
			if MinDamage < 1 : MinDamage = min(1, MaxDamage)
			if MinDamage > MaxDamage : MinDamage = MaxDamage - 1
		if Level == 4 :
			AttackSkill =  CorrectValueWithinRange(AttackSkill,  6, 14)
			DefenceSkill = CorrectValueWithinRange(DefenceSkill, 6, 13)
			MaxDamage =    CorrectValueWithinRange(MaxDamage,    1, 13)
			HitPoints =    CorrectValueWithinRange(HitPoints,   18, 66)
			if MinDamage < 1 : MinDamage = min(1, MaxDamage)
			if MinDamage > MaxDamage : MinDamage = MaxDamage - 1
		if Level == 5 :
			AttackSkill =  CorrectValueWithinRange(AttackSkill,  7, 17)
			DefenceSkill = CorrectValueWithinRange(DefenceSkill, 7, 17)
			MaxDamage =    CorrectValueWithinRange(MaxDamage,    3, 22)
			HitPoints =    CorrectValueWithinRange(HitPoints,   27, 77)
			if MinDamage < 3 : MinDamage = min(3, MaxDamage)
			if MinDamage > MaxDamage : MinDamage = MaxDamage - 1
		if Level == 6 :
			AttackSkill =  CorrectValueWithinRange(AttackSkill,  11, 19)
			DefenceSkill = CorrectValueWithinRange(DefenceSkill, 11, 19)
			MaxDamage =    CorrectValueWithinRange(MaxDamage,     9, 33)
			HitPoints =    CorrectValueWithinRange(HitPoints,    63, 132)
			if MinDamage < 9 : MinDamage = min(9, MaxDamage)
			if MinDamage > MaxDamage : MinDamage = MaxDamage - 1
		if Level == 7 :
			AttackSkill =  CorrectValueWithinRange(AttackSkill,  15, 33)
			DefenceSkill = CorrectValueWithinRange(DefenceSkill, 15, 33)
			MaxDamage =    CorrectValueWithinRange(MaxDamage,    23, 66)
			HitPoints =    CorrectValueWithinRange(HitPoints,   135, 330)
			if MinDamage < 23 : MinDamage = min(23, MaxDamage)
			if MinDamage > MaxDamage : MinDamage = MaxDamage - 1
	
		ReplaceValue(FileContent, JSONfields[4], AttackSkill);
		ReplaceValue(FileContent, JSONfields[5], DefenceSkill);
		ReplaceValue(FileContent, JSONfields[6], HitPoints);
		ReplaceValueMinMax(FileContent, JSONfields[7], MinDamage, MaxDamage);	

	return [AttackSkill, DefenceSkill, HitPoints, MaxDamage, MinDamage]

def GetValueOfAbility(FileContent, AbilityName):
	found = False
	for Line in FileContent :
		if isNotCommentedOut(Line, '"abilities"') :
			found = True
		if found :
			if isNotCommentedOut(Line, JSONfields[2]) :
				return ExtractValue(Line, JSONfields[2])
			if Line.count('}') :
				found = False
	return -1

# Main procedure balancing files
def CorrectValues(FileContent):
	Level = GetValueFromList(FileContent, JSONfields[3])
	DefenceSkill = GetValueFromList(FileContent, JSONfields[5])
	AttackSkill = GetValueFromList(FileContent, JSONfields[4])
	HitPoints = GetValueFromList(FileContent, JSONfields[6])	
	Speed = GetValueFromList(FileContent, JSONfields[8])
	
	IsTwoHex = GetBooleanAbilityExistence(FileContent, '"TWO_HEX_BREATH_ATTACK"')
	IsPoison = GetBooleanAbilityExistence(FileContent, '"POISON"')
	isShooter = GetBooleanAbilityExistence(FileContent, '"SHOOTER"')
	IsAcidBreath = GetBooleanAbilityExistence(FileContent, '"ACID_BREATH"');
	IsDoubleDamage = GetBooleanAbilityExistence(FileContent, '"DOUBLE_DAMAGE_CHANCE"')
	IsMinimumDamage = GetBooleanAbilityExistence(FileContent, '"ALWAYS_MINIMUM_DAMAGE"')
	IsMaximumDamage = GetBooleanAbilityExistence(FileContent, '"ALWAYS_MAXIMUM_DAMAGE"')
	IsAdditionalAttack = GetBooleanAbilityExistence(FileContent, '"ADDITIONAL_ATTACK"')
	IsThreeHeadedAttack = GetBooleanAbilityExistence(FileContent, '"THREE_HEADED_ATTACK"')
	IsAttacksAllAdjacent = GetBooleanAbilityExistence(FileContent, '"ATTACKS_ALL_ADJACENT"')
	IsEnemyDefenceReduction = GetBooleanAbilityExistence(FileContent, '"ENEMY_DEFENCE_REDUCTION"')
	IsGeneralAttackReduction = GetBooleanAbilityExistence(FileContent, '"GENERAL_ATTACK_REDUCTION"')

	MinMax = GetMaxMinFromList(FileContent, JSONfields[7])
	MinDamage = MinMax[1]
	MaxDamage = MinMax[0]
	
	Params = [AttackSkill, DefenceSkill, HitPoints, MaxDamage, MinDamage, Level]	
	OutParams = BalanceProcedure(FileContent, Params)
	
	AttackSkill  = OutParams[0]
	DefenceSkill = OutParams[1]
	HitPoints    = OutParams[2]
	MaxDamage    = OutParams[3]
	MinDamage	 = OutParams[4]
	
	IsUpgraded = not GetBooleanAbilityExistence(FileContent, JSONfields[9])
	
	MinQuantity = MaxQuantity = 0
	
	if 0 < Level <= 7 :		
		if Level == 1 :
			if IsUpgraded :
				MaxQuantity = 30
				MinQuantity = 20
			else:
				MaxQuantity = 50
				MinQuantity = 20
		if Level == 2 :
			if IsUpgraded :
				MaxQuantity = 25
				MinQuantity = 16
			else:
				MaxQuantity = 30
				MinQuantity = 25
		if Level == 3 :
			if IsUpgraded :
				MaxQuantity = 20
				MinQuantity = 12
			else:
				MaxQuantity = 25
				MinQuantity = 12
		if Level == 4 :
			if IsUpgraded :
				MaxQuantity = 16
				MinQuantity = 10
			else:
				MaxQuantity = 20
				MinQuantity = 10
		if Level == 5 :
			if IsUpgraded :
				MaxQuantity = 12
				MinQuantity = 8
			else:
				MaxQuantity = 16
				MinQuantity = 8
		if Level == 6 :
			if IsUpgraded :
				MaxQuantity = 10
				MinQuantity = 5
			else:
				MaxQuantity = 12
				MinQuantity = 5
		if Level == 7 :
			if IsUpgraded :
				MaxQuantity = 8
				MinQuantity = 3
			else:
				MaxQuantity = 10
				MinQuantity = 4
	
	ReplaceValueMinMax(FileContent, JSONfields[10], MinQuantity, MaxQuantity)
	
	CorrMaxDamage = MaxDamage
	CorrMinDamage = MinDamage
	
	if IsMinimumDamage : CorrMaxDamage = MinDamage
	if IsMaximumDamage : CorrMinDamage = MaxDamage
	if IsThreeHeadedAttack : CorrMaxDamage *= 3
	if IsAttacksAllAdjacent: CorrMaxDamage *= 6
	if IsAdditionalAttack  : CorrMaxDamage *= 2
	if IsTwoHex            : CorrMaxDamage *= 2
	if IsAcidBreath        : CorrMaxDamage += GetValueOfAbility(FileContent, '"ACID_BREATH"')
	if IsPoison            : CorrMaxDamage += GetValueOfAbility(FileContent, '"POISON"')
	if IsDoubleDamage :
		DoubleDamageChance = GetValueOfAbility(FileContent, '"DOUBLE_DAMAGE_CHANCE"')
		if DoubleDamageChance > 0 :
			CorrMaxDamage += MaxDamage
	
	EnemyDefenceReduction = 0.0
	GeneralAttackReduction = 0.0
	
	if IsEnemyDefenceReduction :
		EnemyDefenceReduction = GetValueOfAbility(FileContent, '"ENEMY_DEFENCE_REDUCTION"') / 100.0
		if EnemyDefenceReduction >= 1.0 : EnemyDefenceReduction = 1.0
	if IsGeneralAttackReduction :
		GeneralAttackReduction = GetValueOfAbility(FileContent, '"GENERAL_ATTACK_REDUCTION"') / 100.0
		if GeneralAttackReduction >= 1.0 : GeneralAttackReduction = 1.0
	
	Out = calculateValues(AttackSkill, DefenceSkill, HitPoints, CorrMinDamage, \
                          CorrMaxDamage, GeneralAttackReduction, EnemyDefenceReduction)
	FightValue = Out[0]
	AIValue    = Out[1]
	
	CorrFightValue = FightValue
	CorrAIValue    = AIValue
	
	for ability in Abilities:
		if GetBooleanAbilityExistence(FileContent, '"' + ability[0] + '"'):
			CorrFightValue = CorrFightValue * ((100 + ability[1]) / 100.0)
			CorrAIValue    = CorrAIValue    * ((100 + ability[2]) / 100.0)
	
	if Speed > 5 :
		if Speed <= 10 :
			CorrFightValue *= 1.05
			CorrAIValue *= 1.05
		else:
			CorrFightValue *= 1.10
			CorrAIValue *= 1.10
	
	ReplaceValue(FileContent, JSONfields[11], int(CorrAIValue))
	ReplaceValue(FileContent, JSONfields[12], int(CorrFightValue))
	
	return FileContent

def isJSON(FileName):
	if FileName.lower().endswith('.json'):
		return True
	return False

def getDirORFileName(String):
	return os.path.basename(String)

def writeNewFileAndCloseIt(FileHandle, FileContent):
	for fileLines in FileContent:
		FileHandle.write(fileLines + '\n')
	FileHandle.close()

def prepareJSONs():
	os.chdir(os.path.dirname(sys.argv[0]))
	if not os.path.exists(BalancedJSONsFolderName[0]):
		os.makedirs(BalancedJSONsFolderName[0])
	for file in range(len(sys.argv)):
		if file == 0:
			continue
		if os.path.isdir(sys.argv[file]):
			dirName = sys.argv[file] # full path to folder
			dirNameFiles = os.listdir(dirName) #all files in folder
			if not os.path.exists(BalancedJSONsFolderName[0] + '\\' + getDirORFileName(dirName)):
				os.makedirs(BalancedJSONsFolderName[0] + '\\' + getDirORFileName(dirName))
			for dirFile in dirNameFiles:			
				if isJSON(dirFile):
					FileContent = readSpecifiedFile(dirName + '\\' + dirFile)
					FileContent = CorrectValues(FileContent)
					BalancedFileToSave = open(BalancedJSONsFolderName[0] + '\\' + \
                                         getDirORFileName(dirName) + '\\' + dirFile, 'w+')
					
					writeNewFileAndCloseIt(BalancedFileToSave, FileContent)
			continue
		if isJSON(sys.argv[file]):
			FileContent = readSpecifiedFile(sys.argv[file])
			FileContent = CorrectValues(FileContent)
			BalancedFileToSave = open(BalancedJSONsFolderName[0] + '\\' + getDirORFileName(sys.argv[file]), 'w+')
			
			writeNewFileAndCloseIt(BalancedFileToSave, FileContent)


prepareJSONs()

raw_input("Done. Press ENTER...")