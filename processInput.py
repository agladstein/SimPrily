import sys
from collections import OrderedDict
from operator import itemgetter

from main_tools.housekeeping import debugPrint, set_seed
from main_tools.my_random import MY_RANDOM as random

verbos = 0
times = []


def getSampleAndDiscovery(in_file):
    tempFile = readModelFile(in_file)
    out = []
    out_dict = dict()
    for line in tempFile:
        if line.startswith("-I"):
            line = line.split(',')
            out_dict["-I"] = [int(s.strip()) for s in line[2:] if s]
        elif line.startswith("-discovery") or line.startswith("-sample"):
            line = line.split(',')
            out_dict[line[0]] = [int(s.strip()) for s in line[1:] if s]
    return out_dict

def readModelFile(in_file):
    '''
    reads the file into a list 
    :param in_file: a file name as a string
    :return: a list with each line as a single string object 
    '''
    fl = open(in_file, "r")
    info = []
    for line in fl:
        if line.startswith("-"):
            temp = str(line).strip()
            info.append(temp)
        if line.split(",")[0]== "-s":
            temp = str(line).strip()
            set_seed(temp.split(",")[1])
    return info

def readParamsFile(in_file):
    '''
    reads the file into a list 
    :param in_file: a file name as a string
    :return: a list with each line as a single string object 
    '''
    fl = open(in_file, "r")
    modelParamsDict = {}
    for line in fl:
        if "=" in line:
            modelParamsDict[line.split("=")[0].strip()] = line.split("=")[1].strip()
    return modelParamsDict

def getParamValueBounded(modelParamsDict, tempNum, tempLow=False):
    tempVar = ""
    if tempNum in modelParamsDict.keys():
        tempVar = tempNum 
        tempNum = modelParamsDict[tempNum]

    tempNum = tempNum.strip()
    if ":" not in tempNum:
        tempNum = str(sci_to_float(tempNum))
        returnValue = str(tempNum)
    else:
        # This means you want range
        tempLow = max(float(sci_to_float(tempNum.split(":")[0][1:])),float(tempLow))
        tempHigh = sci_to_float(tempNum.split(":")[1][:-1])
        returnValue = str(random.uniform(float(tempLow),float(tempHigh)))
    if tempVar in modelParamsDict.keys():
        modelParamsDict[tempVar] = returnValue
    return returnValue

def priorToParamValue(inputParamStr):
    '''
    priorToParamValue:
    This is a helper function that takes a string in the form (###:###)
    Numbers are allowed to be either scientfic notation or base 10
    And returns a random value in that range, in the form of a string
    '''
    assert(type(inputParamStr) == type("")),"priorToParamValue called without a string"

    tempLow = float(sci_to_float(inputParamStr.split(":")[0][1:]))
    tempHigh = float(sci_to_float(inputParamStr.split(":")[1][:-1]))
    returnValue = str(random.uniform(tempLow,tempHigh))
    return returnValue


def getParamValueUnBounded(modelParamsDict, paramKey):
    '''
    getParamValueUnBounded:
    This is a function that searches the model dictionary for the value 
    and replace the param name with the matching param value in the param file
    If there is a value that is a given range it will pick a float in that range
    '''
    # TODO, add assert for that if later
    if paramKey in modelParamsDict.keys():
        # tempVar = paramKey 
        paramRawValue = modelParamsDict[paramKey]
        # Strip is here to remove any whitespace that might be in param file
        # TODO: This strip should be done when we make the dictionary
        paramRawValueStriped = paramRawValue.strip()
        if ":" in paramRawValueStriped:
            # This means you want range
            unscaledParamValue = priorToParamValue(paramRawValueStriped)
        else:
            unscaledParamValue = str(sci_to_float(paramRawValueStriped))
        # Updating the Params dict with the chosen value 
        modelParamsDict[paramKey] = unscaledParamValue
    else:
        # TODO, this else needs to be removed...if it goes
        # into this else, this function shouldn't have been called
        print("paramKey: {}".format(paramKey))
        unscaledParamValue = paramKey
    return unscaledParamValue

def sci_to_float(s):
    """
    Converts a string of the form 'aEb' into an int given by a*10^b
    """
    s = s.replace("e","E")
    if 'E' in s:
        s = s.split('E')
        return float(s[0]) * 10**float(s[1])
    return s

def findScaleValue(flags, modelParamsDict):
    # used for scaling
    debugPrint(2, "Finding scaling value")
    Ne=10000
    if "-Ne" not in flags.keys():
        if "-n" in flags.keys():
            Ne=float(getParamValueUnBounded(modelParamsDict, flags["-n"][0][1]))
    else:
        Ne = float(getParamValueUnBounded(modelParamsDict, flags['-Ne'][0][0]))
    debugPrint(2,"Scaling factor found: {0}".format(Ne))
    return Ne

def processTimeData(flag, lastTime, modelParamsDictRaw, timeDataRaw):
    '''
    This is a helper function that takes the raw time data from the model
    file and replaces it with the correct value in the params file.

    '''
    if "_" in flag: 
        if int(flag.split("_")[1]) == 1:
            # First time through, no bounds outside of given in param Value
            lowTime = False
        else:
            # There is a low time bound on the random range
            lowTime = True
    else:
        # There is no time constrant
        lowTime = False

    if "inst" in timeDataRaw:
        tempTime = str(float(lastTime) + 1)
        while tempTime in times:
            tempTime += 1
        timeData = tempTime
    else:
        if lowTime:
            timeData = getParamValueBounded(modelParamsDictRaw, timeDataRaw, lastTime)
        else:
            timeData = getParamValueUnBounded(modelParamsDictRaw, timeDataRaw)

    return timeData

def populateFlags(modelParamsDictRaw, modelDataRaw):
    '''
    This will fill a dictionary with keys that equal the flags, and values that
    is a list of every time (in order) the flag is used.
    '''
    debugPrint(2, "Starting: populateFlags ")
    modelData = []
    flags = OrderedDict()
    lowTime = False
    # loops through all items in modelDataRaw
    for i, argument in enumerate(modelDataRaw):
        argSplit = argument.split(',')

        flag = argSplit[0]
        # if flag starts with -e it will be an event flag, thus, the order must be preserved
        if flag.startswith("-e"):
            # striping any random whitepace
            # TODO: The line spit should be done before this part
            timeDataRaw = argSplit[1].strip()
            lastTimeValue = modelData[i-1].split(',')[1]
            timeData = processTimeData(flag, lastTimeValue, modelParamsDictRaw, timeDataRaw)

            times.append(timeData)
            argSplit[1] = timeData
            flag = argSplit[0].split("_")[0]

        if flag in flags.keys():
            flags[flag].append([x.strip() for x in argSplit[1:] if x])
        else:
            flags[flag] = [[x.strip() for x in argSplit[1:] if x]]

        modelData.append(",".join(argSplit))

    modelParamsDict = modelParamsDictRaw

    return flags, modelParamsDict, modelData

def processType1Flags(flag, argument, processedData, modelParamsDictRaw):
    '''
    This is a helper function fpr processing input files. 
    It takes a flag, arguments, and returns an updated processedData
    '''

    if flag == "-discovery":
        processedData['discovery'] = [int(s.strip()) for s in argument if s]
    if flag == "-sample":
        processedData['sample'] = [int(s.strip()) for s in argument if s]
    if flag == "-daf":
        processedData['daf'] = float(getParamValueUnBounded(modelParamsDictRaw, argument[0]))
    if flag == "-length":
        processedData['length'] = argument[0]
    if flag == "-macs":
        processedData['macs'] = argument[0]
    if flag == "-I":
        processedData["I"] = [int(s.strip()) for s in argument[1:] if s]
    if flag == "-macsswig":
        processedData['macsswig'] = argument[0]
    if flag == "-n":
        tmp = processedData.get('name', [])
        tmp.append(argument[1])
        processedData['name'] = tmp

    return processedData


def scaleArgument(flag, argumentRaw, Ne, modelParamsDictRaw):
    '''
    A helper function that scaled one index in the arguhemt. 
    It returns the scaled number and the index the scaled numbers goes to. 
    To add more flags to this, add it to the matching index group and matching scale group
    '''

    # Get the index for the value you are changing
    index0 = ["-t","-r","-G"]
    if flag in index0:
        index = 0
    index1 = ["-eM","-g","-eN","-n"]
    if flag in index1:
        index = 1

    index2 = ["-en","-eg","-es","-m", "-em"]
    if flag in index2:
        index = 2

    index3 = ["-em"]
    if flag in index3:
        index = 3

    # Get the param value if needed
    if argumentRaw[index] in modelParamsDictRaw:
        param = getParamValueUnBounded(modelParamsDictRaw, argumentRaw[index])
    else:
        # If the flag isn't in param, no need to call it
        param = argumentRaw[index]

    # scale the number when we have it
    scaleFactor1 = [
        "-em","-eM","-g","-eg","-m","-t","-r","-G",
    ]
    scaleFactor2 = ["-eN", "-n", "-en"]

    if flag in scaleFactor1:
        scaledParam = str(float(4*(float(param)*Ne)))
    elif flag in scaleFactor2:
        scaledParam = str(float((float(param)/Ne)))
    else:
        scaledParam = param

    return scaledParam, index


def processInputFiles(paramFile, modelFile, args):
    '''
    This is the function that takes links to two files and outputs a dictionay (processedData)
    With all the (useful) data in the two files
    '''
    debugPrint(2, "Starting processInputFiles")
    
    modelDataRaw = readModelFile(modelFile)
    debugPrint(2, "Finished reading " + str(modelFile))
    debugPrint(3, "Raw input data into make_args", modelDataRaw)

    modelParamsDictRaw = readParamsFile(paramFile)
    debugPrint(2, "Finished reading " + str(paramFile))
    
    debugPrint(3,"Raw Output for modelParamsDict", modelParamsDictRaw)


    processedData = {}
    
    flags, modelParamsDict, modelData = populateFlags(modelParamsDictRaw, modelDataRaw)
    Ne = findScaleValue(flags, modelParamsDictRaw)

    if flags['-random_discovery']:
        if '-macs_file' in flags:
            macs_args = [flags['-macs_file'][0][0], flags['-length'][0][0], "-I", flags['-I'][0][0]]
        elif '-macsswig' in flags:
              macs_args = [flags['-macsswig'][0][0], flags['-length'][0][0], "-I", flags['-I'][0][0]]
        elif '-macs' in flags:
            macs_args = [flags['-macs'][0][0], flags['-length'][0][0], "-I", flags['-I'][0][0]]
        sizes = map(int, flags["-I"][0][1:])
        if (sys.version_info > (3, 0)):
            sizes = list(sizes)
        for discovery_pop_str in flags["-discovery"][0]:
            discovery_pop = int(discovery_pop_str)-1
            sizes[discovery_pop] += random.randint(2, sizes[discovery_pop])
        total = float(sum(sizes))
        macs_args.insert(1,str(total))
        sizes_str = map(str, sizes)
        if (sys.version_info > (3, 0)):
            sizes_str = list(sizes_str)
        macs_args.extend(sizes_str)
        
    else:
        # creates a total value from the <n_n> values (from -I)
        numlist = [float(x) for x in flags['-I'][0][1:]]
        total = sum(numlist)
        macs_args = [flags['-macs'][0][0], str(total), flags['-length'][0][0], "-I"]
        for genotyped_size in flags["-I"][0]:
            macs_args.append(genotyped_size)


    # seasons is all the time based events
    seasons = []

    # processOrderedSeasons(flags, modelParamsDict)
    debugPrint(3,"Processing flags in for macs_args")
    for flag in flags.keys():
        # Looping through every key
        debugPrint(3,"FLAG:  {}: {}".format(flag,flags[flag]))
        for argumentRaw in flags[flag]:
            print("argumentRaw: {}".format(argumentRaw))
            # Looping through every argumentRaw
            try:
                debugPrint(3,flag + ": " + str(argumentRaw))
                ignoredFlags = ["-germline",
                                "-array",
                                "-nonrandom_discovery",
                                "-random_discovery",
                                "-pedmap"]

                if flag in ignoredFlags:
                    continue

                type1Flags = [
                    "-discovery", "-sample", "-daf", "-length", "-macs", "-I", "-macsswig", "-n",
                ]
                if flag in type1Flags:
                    processedData = processType1Flags(flag, argumentRaw, processedData, modelParamsDictRaw)
                    continue

                # Seed is a specal case. 
                if flag == "-s":
                    processedData['seed'] = argumentRaw[0]

                type2Flags = [
                    "-em","-eM","-g","-eN","-n","-en","-eg","-es","-m","-t","-r","-G"
                ]

                if flag in type2Flags:
                    scaledParam, index = scaleArgument(flag, argumentRaw, Ne, modelParamsDictRaw)
                    argumentRaw[index] = scaledParam
                    argument = argumentRaw

                # These scales are difference since they scale all possible values in list
                if flag == "-ema":
                    scaledParams = argumentRaw[:1]
                    for i in range(2,len(argumentRaw)):
                        param = getParamValueUnBounded(modelParamsDictRaw, argumentRaw[i])
                        scaledParams.append(str(float(4*(float(param)*Ne))))
                    argument = scaledParams
                elif flag == "-ma":
                    scaledParams = argumentRaw[0]
                    for i in range(len(argumentRaw)):
                        param = getParamValueUnBounded(modelParamsDictRaw, argumentRaw[i])
                        scaledParams.append(str(float(4*(float(param)*Ne))))
                    argument = scaledParams

                if flag.startswith('-e'):
                    # all <t>'s are scaled
                    pass
                    argumentRaw[0] = getParamValueUnBounded(modelParamsDictRaw, argumentRaw[0])
                    argumentRaw[0]=str(round(float(argumentRaw[0]))/(4*Ne))
                    seasons.append([flag] + argumentRaw)
                
                else:
                    macs_args.append(flag.strip())
                    for subLine in argumentRaw:
                        macs_args.append(subLine.strip())
            except IndexError as e:
                print("There was an index error!\nThis most likely means your input file has a malformed flag.")
                print("Try running with -vv argument for last flag ran")
                sys.exit()

    if '-n' not in flags:
        tmp = list(range(1,int(flags['-I'][0][0])+1))
        processedData['name'] = tmp

    if not processedData.get('discovery') or not processedData.get('sample') or not processedData.get('daf'):
        if not processedData.get('discovery') and not processedData.get('sample') and not processedData.get('daf'):
            print("discovery, sample, and daf are all missing")
        else:
            print("discovery, sample, or daf is missing")
            quit()
            

    debugPrint(2, "Adding events data back to flag pool")
    for i in range(len(seasons)):
        seasons[i][1] = float(seasons[i][1])
    seasons = sorted(seasons, key=itemgetter(1))
    for i in range(len(seasons)):
        seasons[i][1] = str(seasons[i][1])
    for season in seasons:
        macs_args.extend(season)

    processedData["macs_args"] = macs_args

    debugPrint(3,"Priting modelParamsDict:", modelParamsDict)

    processedData['param_dict'] = modelParamsDict

    if args['genetic map']:
        processedData['macs_args'].extend(['-R', args['genetic map']])

    return processedData


