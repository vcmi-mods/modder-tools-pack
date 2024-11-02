#How to run this script?
# Via command prompt:
#	1. Open command prompt and set working directory same as path to this script
#	2. Type name of this script
#	3. Drag and drop valid H3 RMG template file(usually with *.txt extension).
#	You also can specify many files by repeating step 3. but remember to separate them by space
# Via dropping files and folders with H3 RMG templates over script icon

#Important note:
# There may still be some bugs regarding parsing H3 templates, so best way to avoid/fix them is to copy
#  whole file into editor like Calc from Open Office or Excel from MS Office(not sure about this one),
#  select all lines (CTRL+A) and copy/paste them back to first file.

#Script author: Kantor

#Usefull links:
# http://heroescommunity.com/viewthread.php3?TID=7769&PID=139382#focus
# http://heroescommunity.com/viewthread.php3?TID=14290&PID=286557#focus
# http://heroescommunity.com/viewthread.php3?TID=7114&PID=297329#focus
# http://heroescommunity.com/viewthread.php3?TID=3146&PID=59392#focus
# http://forum.heroesworld.ru/showpost.php?p=564869&postcount=42

import os
import sys

WORKING_DIR = os.path.dirname(sys.argv[0])
PARAMETERS = sys.argv[1:]
OUTPUT_FOLDER_NAME = 'Converted'
RAW_RMG_DATA = []

def readFile(FileName):
	file = open(FileName, 'r')
	content = [text.strip('\n') for text in file.readlines()]
	file.close()
	
	return content

def getName(String):
	return os.path.basename(String)

def writeNewFileAndCloseIt(FileHandle, Content):
	for fileLines in Content:
		FileHandle.write(fileLines + '\n')
	FileHandle.close()

def createDirIfNeeded(Location):
	if not os.path.exists(Location):
		os.makedirs(Location)

def extract_RMG_Info():
	global RAW_RMG_DATA
	
	RAW_RMG_DATA = [RAW_RMG_DATA[i][:85] for i in range(len(RAW_RMG_DATA))]
	RAW_RMG_DATA = [line for line in RAW_RMG_DATA if line.count('') != len(line)]
	
	listOfTemplates = []
	header = RAW_RMG_DATA[:3]
	
	positions = [index for index in range(3, len(RAW_RMG_DATA)) if RAW_RMG_DATA[index][0] != '']
	print('Templates found:', len(positions))
	
	temp = range(len(positions))
	for index in temp:
		if index != temp[-1]:
			listOfTemplates += [header[:] + RAW_RMG_DATA[positions[index]:positions[index + 1]]]
		else:
			listOfTemplates += [header[:] + RAW_RMG_DATA[positions[index]:]]
	
	for index in range(len(listOfTemplates)):
		RMGInfo = {}	
		#Each level represents 1st, 2nd and 3rd row in OH3 RMG Template file
		level0 = level1 = Level2 = ''
		for i in range(len(listOfTemplates[index][0])):
			if listOfTemplates[index][0][i] != '':
				level0 = listOfTemplates[index][0][i]
			if listOfTemplates[index][1][i] != '':
				level1 = listOfTemplates[index][1][i]
			if listOfTemplates[index][2][i] != '':
				level2 = listOfTemplates[index][2][i]
			#if RMGInfo.has_key(level0) == False: <-- obsolete in Python 3.x.x
			if level0 not in RMGInfo:
				RMGInfo[level0] = {}
			#if RMGInfo[level0].has_key(level1) == False: <-- obsolete in Python 3.x.x
			if level1 not in RMGInfo[level0]:
				RMGInfo[level0][level1] = {}
			#if RMGInfo[level0][level1].has_key(level2) == False: <-- obsolete in Python 3.x.x
			if level2 not in RMGInfo[level0][level1]:
				RMGInfo[level0][level1][level2] = []
			
			for col in range(3, len(listOfTemplates[index])):
				RMGInfo[level0][level1][level2] += [listOfTemplates[index][col][i]]		
		
		maxTreasures = len(RMGInfo['Zone']['']['Id'])
		queue = ['Low', 'High', 'Density']
		for val in queue:
			treasure = []
			for i in range(3): #0-2 because [Low/High/Density] occurs 3 times
				treasure += [RMGInfo['Zone']['Treasure'][val][:maxTreasures]]
				RMGInfo['Zone']['Treasure'][val] = RMGInfo['Zone']['Treasure'][val][maxTreasures:]
			RMGInfo['Zone']['Treasure'][val] = treasure[:3]
			
		listOfTemplates[index] = RMGInfo.copy()
	
	return listOfTemplates

def getConnections(RMGInfo):
	connections = '\t\t\"connections\" :\n\t\t[\n__FIELDS__\t\t]'
	toFill = '\t\t\t{ \"a\" : \"__PORTAL_A__\", \"b\" : \"__PORTAL_B__\", \"guard\" : __GUARD__ }__,__\n'
	result = ''
	
	zoneA = RMGInfo['Connections']['Zones']['Zone 1']
	zoneB = RMGInfo['Connections']['Zones']['Zone 2']
	guard = RMGInfo['Connections']['Zones']['Value']
	for i in range(len(zoneA) - zoneA.count('')):
		zoneA[i] = (zoneA[i].replace('.', ',')).replace(' ', '')
		zoneB[i] = (zoneB[i].replace('.', ',')).replace(' ', '')
		zA = zoneA[i].split(',')[1:] if ',' in zoneA[i] else []
		zB = zoneB[i].split(',')[1:] if ',' in zoneB[i] else []
		if ',' in zoneA[i]: zoneA[i] = zoneA[i][:zoneA[i].index(',')]
		if ',' in zoneB[i]:	zoneB[i] = zoneB[i][:zoneB[i].index(',')]
		
		for items in zA:
			zoneA += items
			zoneB += [zoneB[i]]
			guard += [guard[i]]
		for items in zB:
			zoneA += [zoneA[i]]
			zoneB += items
			guard += [guard[i]]
	
	quantity = range(len(zoneA) - zoneA.count(''))
	occurrences = []
	for i in quantity:
		if zoneA[i] == zoneB[i]:
			continue
		temp = toFill.replace('__PORTAL_A__', zoneA[i])
		temp = temp.replace('__PORTAL_B__', zoneB[i])
		temp = temp.replace('__GUARD__', guard[i]) if guard[i] != '' else temp.replace('__GUARD__', '0')
		if i == quantity[-1]:
			temp = temp.replace('__,__', '')
		else:
			temp = temp.replace('__,__', ',')
		pair = [zoneA[i], zoneB[i]]
		if not (pair in occurrences) and  not (pair[::-1] in occurrences):
			occurrences += [pair]
			result += temp
	if result[-2] == ',':
		result = result[:result.rindex(',')] + result[result.rindex(',') + 1:]
	
	return connections.replace('__FIELDS__', result)

def getZoneType(RMGInfo, index):
	toFill = '\t\t\t\t\"type\" : \"__TYPE__\",\n'
	zoneType = RMGInfo['Zone']['Type']
	
	if zoneType['human start'][index] == 'x':
		return toFill.replace('__TYPE__', 'playerStart')
	elif zoneType['computer start'][index] == 'x':
		return toFill.replace('__TYPE__', 'cpuStart')
	elif zoneType['Treasure'][index] == 'x':
		return toFill.replace('__TYPE__', 'treasure')
	elif zoneType['Junction'][index] == 'x':
		return toFill.replace('__TYPE__', 'junction')
	else: #sometimes may happen that type isn't defined, what then?
		return toFill.replace('__TYPE__', 'treasure')

def getZoneSize(RMGInfo, index):
	toFill = '\t\t\t\t\"size\" : __SIZE__,\n'
	zoneSize = RMGInfo['Zone']['Type']['Base Size'][index]
	
	return toFill.replace('__SIZE__', zoneSize)

def getZoneOwner(RMGInfo, index):
	toFill = '\t\t\t\t\"owner\" : __OWNER__,\n'
	zoneOwner = RMGInfo['Zone']['Player towns']['Ownership'][index]
	
	return toFill.replace('__OWNER__', zoneOwner) if zoneOwner != '' else ''

def getMonsterStr(RMGInfo, index):
	toFill = '\t\t\t\t\"monsters\" : \"__STRENGTH__\",\n'
	monsterStrength = RMGInfo['Zone']['Monsters']['Strength'][index]	
	
	if monsterStrength.lower() == 'avg' or monsterStrength.lower() == 'average':
		return toFill.replace('__STRENGTH__', 'normal')
	elif monsterStrength.lower() != 'none':
		return toFill.replace('__STRENGTH__', monsterStrength)
	return toFill.replace('__STRENGTH__', 'normal')

def getZoneMines(RMGInfo, index):
	toFill = '\t\t\t\t\"mines\" : { __MINES__ },\n'
	minesLikeZone = '\t\t\t\t\"minesLikeZone\" : __INDEX__,\n'
	minesInZone = RMGInfo['Zone']['Minimum mines']
	allMines = ['Wood', 'Mercury', 'Ore', 'Sulfur', 'Crystal', 'Gems', 'Gold']
	
	tempMines = []
	temp = []
	for mine in allMines:
		tempMines += [minesInZone[mine][index]] if ' ' not in minesInZone[mine][index] else ''
		if minesInZone[mine][index] != '' and ' ' not in minesInZone[mine][index]:
			temp += ['\"' + mine.lower() + '\" : ' + minesInZone[mine][index]]
	
	for lowerIndex in range(index):
		checkIfExists = []
		for mine in allMines:
			checkIfExists += [minesInZone[mine][lowerIndex]]
		if tempMines == checkIfExists and checkIfExists.count('') != len(allMines):
			return minesLikeZone.replace('__INDEX__', str(lowerIndex + 1))

	if len(temp) > 0:
		temp = (str(temp).strip('[]')).replace('\'', '')
		return toFill.replace('__MINES__', temp)
	return ''

def getTownsAreOfSameType(RMGInfo, index):
	toFill = '\t\t\t\t\"townsAreSameType\" : __YESNO__,\n'
	sameType = RMGInfo['Zone']['Neutral towns']['Towns are of same type'][index]
	
	return toFill.replace('__YESNO__', 'true') if sameType == 'x' else ''

def getHumanORNeutralTowns(RMGInfo, index):
	toFill = '\t\t\t\t\"__WHO__\" : { __SET__ },\n'
	owners = ['playerTowns', 'neutralTowns']
	townInfo = RMGInfo['Zone']
	result = ''
	
	whoseTown = ['Player towns', 'Neutral towns']
	for who in whoseTown:
		temp = []
		town = townInfo[who]
		if town['Minimum towns'][index] != '':
			temp += ['"towns" : ' + town['Minimum towns'][index]]
		if town['Minimum castles'][index] != '':
			temp += ['"castles" : ' + town['Minimum castles'][index]]
		if len(temp) > 0:
			result += toFill.replace('__WHO__', owners[whoseTown.index(who)])
			result = result.replace('__SET__', (str(temp).strip('[]'))).replace('\'', '')

	return result if len(result) > 0 else ''

def getAllowedFactions(RMGInfo, index):
	toFill = '\t\t\t\t\"__WHAT__\" : [ __SET__ ],\n'
	allowedWhat = ['allowedTowns', 'allowedMonsters']
	allowed = RMGInfo['Zone']
	result = ''
	
	commonTowns = ['Castle', 'Rampart', 'Tower', 'Inferno', 'Necropolis', 'Dungeon', 'Stronghold', 'Fortress']
	whatIsNow = ['Town types', 'Monsters']
	for what in whatIsNow:
		if what == 'Town types':
			factions = commonTowns[:] + ['Elemental']
		else:
			factions = commonTowns[:] + ['Neutral', 'Forge']
		
		backup = factions[:]
		foo = []
		for i in factions:
			if allowed[what][i][index] == 'x':
				foo += [i]
		factions = foo[:]
		
		if factions != backup and len(factions) > 0:
			if what == 'Town types':
				if 'Elemental' in factions:
					factions[factions.index('Elemental')] = 'conflux'
			else:
				if 'Forge' in factions:
					factions[factions.index('Forge')] = 'conflux'
					
			for i in range(len(factions)):
				factions[i] = '\"' + factions[i].lower() + '\"'
			
			result += toFill.replace('__WHAT__', allowedWhat[whatIsNow.index(what)])
			result = result.replace('__SET__', (str(factions).strip('[]')).replace('\'', ''))
	
	return result if len(result) > 0 else ''

def getTerrains(RMGInfo, index):
	toFill = '\t\t\t\t\"terrainTypes\" : [ __TTYPE__ ],\n'
	doesMatch = '\t\t\t\t\"matchTerrainToTown\" : __YESNO__,\n'
	terrainLikeZone = '\t\t\t\t\"terrainTypeLikeZone\" : __INDEX__,\n'
	matchingToTown = RMGInfo['Zone']['Terrain']['Match to town']
	allowedTerr = RMGInfo['Zone']['Terrain']	
	result = ''
	
	temp = []
	terrains = ['Dirt', 'Sand', 'Grass', 'Snow', 'Swamp', 'Rough', 'Cave', 'Lava']
	for type in terrains:		
		if allowedTerr[type][index] == 'x':
			temp += [type]
	
	if matchingToTown[index] != 'x':
		result += doesMatch.replace('__YESNO__', 'false')
	
	for lowerIndex in range(index):
		checkIfExists = []
		for type in terrains:
			if allowedTerr[type][lowerIndex] == 'x':
				checkIfExists += [type]
		if temp == checkIfExists:
			if matchingToTown[lowerIndex] == matchingToTown[index] != 'x':
				if checkIfExists != terrains and len(checkIfExists) > 0:
					return terrainLikeZone.replace('__INDEX__', str(lowerIndex + 1))
				else:
					return doesMatch.replace('__YESNO__', 'false')
	
	if temp != terrains:
		if 'Cave' in temp:
			temp[temp.index('Cave')] = 'subterra'
		for i in range(len(temp)):
			temp[i] = '\"' + temp[i].lower() + '\"'
		if len(temp) > 0:
			result += toFill.replace('__TTYPE__', (str(temp).strip('[]')).replace('\'', ''))
	
	return result if len(result) > 0 else ''

def getTreasure(RMGInfo, index):
	toFill = '\t\t\t\t\"treasure\" :\n\t\t\t\t[\n__TREASURES__\t\t\t\t]\n'
	mmd = '\t\t\t\t\t{ \"min\" : Low, \"max\" : High, \"density\" : Density }__,__\n'
	tlz = '\t\t\t\t\"treasureLikeZone\" : __INDEX__,\n'
	treasure = RMGInfo['Zone']['Treasure']
	fields = ['Low', 'High', 'Density']

	treasureSet = ''
	currTreas = []
	for i3 in range(3):
		temp = mmd
		for item in fields:
			if item == 'Density':
				if treasure[item][i3][index] == '0':
					treasure[item][i3][index] = '1'
			currTreas += [treasure[item][i3][index]]
			temp = temp.replace(item, str(treasure[item][i3][index]))
		if treasure['Low'][i3][index] != '':
			treasureSet += temp.replace('__,__', '') if i3 == 2 else temp.replace('__,__', ',')
	
	for lowerIndex in range(index):
		checkIfExists = []
		for i3 in range(3):
			for item in fields:
				checkIfExists += [treasure[item][i3][lowerIndex]]
		if currTreas == checkIfExists and checkIfExists.count('') != 9:
			return tlz.replace('__INDEX__', str(lowerIndex + 1))
		
	if treasureSet != '':
		if treasureSet.count('},') >= treasureSet.count('{'):
			treasureSet = (treasureSet[::-1].replace(',', '', 1))[::-1]
		
		return toFill.replace('__TREASURES__', treasureSet)
	return ''

def getMapSize(RMGInfo):
	toFill = '\t\t\"minSize\" : \"__MIN__\", \"maxSize\" : \"__MAX__\",\n'
	minSize = str(RMGInfo['Map']['']['Minimum Size'][0])
	maxSize = str(RMGInfo['Map']['']['Maximum Size'][0])
	size = {
	  '1' : 's', '2' : 's+u',
	  '4' : 'm', '8' : 'm+u',
	  '9' : 'l', '10' : 'l', '18' : 'l+u',
	  '16' : 'xl', '32' : 'xl+u'
	}
	
	#if size.has_key(min) == False: <-- obsolete in Python 3.x.x
	if minSize not in size:
		min = '1'
	#if size.has_key(max) == False: <-- obsolete in Python 3.x.x
	if maxSize not in size:
		max = '32'
	
	return (toFill.replace('__MIN__', size[minSize])).replace('__MAX__', size[maxSize])

def getPlayers(RMGInfo):
	humansAndCPUs = '\t\t\"players\" : \"__PLAYERS__\", "cpu\" : \"__CPU__\",\n'
	justHumans = '\t\t\"players\" : \"__PLAYERS__\",\n'
	
	players = RMGInfo['Zone']['Type']
	
	humanPlayers = players['human start'].count('x')
	cpuPlayers = players['computer start'].count('x')
	if cpuPlayers > 0:
		return (humansAndCPUs.replace('__PLAYERS__', str(humanPlayers))).replace('__CPU__', str(cpuPlayers))
	else:
		return justHumans.replace('__PLAYERS__', str(humanPlayers))

def fill_VCMI_RMG_Template(RMGInfo):
	fullTemplate = '\n\t\"__TEMPLATE_NAME__\" :\n\t{\n__INFO1____INFO2____ZONES____CONNECTIONS__\n\t}'	
	fullZonesArea = '\t\t\"zones\" :\n\t\t{\n__ALLZONES__\t\t},\n'
	subZone = '\t\t\t\"__ZONE_INDEX__\" :\n\t\t\t{\n__FIELDS__\t\t\t}__,__\n'
	
	templatesContainer = ''
	mapNames = []
	for H3Template in RMGInfo:
		IDs = H3Template['Zone']['']['Id']
		currentZone = ''
		howManyZones = range(len(IDs) - IDs.count(''))
		for i in howManyZones:
			currentZone += subZone.replace('__ZONE_INDEX__', IDs[i])
			if i != howManyZones[-1]:
				currentZone = currentZone.replace('__,__', ',')
			else:
				currentZone = currentZone.replace('__,__', '')
			
			zoneInfo  = getZoneType(H3Template, i)
			zoneInfo += getZoneSize(H3Template, i)
			zoneInfo += getZoneOwner(H3Template, i)
			zoneInfo += getMonsterStr(H3Template, i)
			zoneInfo += getHumanORNeutralTowns(H3Template, i)
			zoneInfo += getTownsAreOfSameType(H3Template, i)
			zoneInfo += getAllowedFactions(H3Template, i)
			zoneInfo += getTerrains(H3Template, i)
			zoneInfo += getZoneMines(H3Template, i)
			zoneInfo += getTreasure(H3Template, i)
			
			if len(zoneInfo) - zoneInfo.rindex(',') == 2:
				colonPos = zoneInfo.rindex(',')
				zoneInfo = zoneInfo[:colonPos] + zoneInfo[colonPos + 1:]
			
			currentZone = currentZone.replace('__FIELDS__', zoneInfo)
		
		mapSize = getMapSize(H3Template)
		players = getPlayers(H3Template)
		mapName = H3Template['Map']['']['Name'][0]
		
		while mapName in mapNames:
			print('Template name', mapName, 'already exists.')
			print('Enter the new one or type \'???\' to display already used names:')
			value = input()
			if value == '???':
				print(mapNames, '\n')
				continue
			if not (value in mapNames):
				mapName = value[:]
		
		mapNames += [mapName]		
		
		completeZones = fullZonesArea.replace('__ALLZONES__', currentZone)
		VCMITemplate = fullTemplate.replace('__TEMPLATE_NAME__', mapName)
		VCMITemplate = VCMITemplate.replace('__INFO1__', mapSize)
		VCMITemplate = VCMITemplate.replace('__INFO2__', players)
		VCMITemplate = VCMITemplate.replace('__ZONES__', completeZones)
		VCMITemplate = VCMITemplate.replace('__CONNECTIONS__', getConnections(H3Template))		
		
		templatesContainer += VCMITemplate
		if H3Template != RMGInfo[-1]:
			templatesContainer += ','
	
	return ['{' + templatesContainer + '\n}']

def prepareRMG():
	global RAW_RMG_DATA
	os.chdir(WORKING_DIR)
	createDirIfNeeded(OUTPUT_FOLDER_NAME)
	for file in range(len(PARAMETERS)):
		del RAW_RMG_DATA[:]
		
		if os.path.isdir(PARAMETERS[file]):
			dirName = PARAMETERS[file] #full path to folder
			dirNameFiles = os.listdir(dirName) #all files in folder
			createDirIfNeeded(OUTPUT_FOLDER_NAME + '\\' + getName(dirName))
			for dirFile in dirNameFiles:
				if dirFile.lower().endswith('.txt'):				
					FileContent = readFile(dirName + '\\' + dirFile)
					for line in FileContent:
						RAW_RMG_DATA += [line.split('\t')]					
					VCMI_Template = fill_VCMI_RMG_Template( extract_RMG_Info() )
					dirFile = dirFile.lower().replace('.txt', '.JSON')
					VCMI_RMG_File = open(OUTPUT_FOLDER_NAME + '\\' + \
                                         getName(dirName) + '\\' + dirFile, 'w+')
					writeNewFileAndCloseIt(VCMI_RMG_File, VCMI_Template)
			continue
		if PARAMETERS[file].lower().endswith('.txt'):			
			FileContent = readFile(PARAMETERS[file])
			for line in FileContent:
				RAW_RMG_DATA += [line.split('\t')]			
			VCMI_Template = fill_VCMI_RMG_Template( extract_RMG_Info() )
			PARAMETERS[file] = PARAMETERS[file].lower().replace('.txt', '.JSON')
			VCMI_RMG_File = open(OUTPUT_FOLDER_NAME + '\\' + getName(PARAMETERS[file]), 'w+')
			writeNewFileAndCloseIt(VCMI_RMG_File, VCMI_Template)


prepareRMG()

input('Done. Press Enter.')