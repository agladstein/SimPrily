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
    variables = {}
    for line in fl:
        if "=" in line:
            variables[line.split("=")[0].strip()] = line.split("=")[1].strip()
    return variables

def getUnscaledValue(variables, tempNum, tempLow=False):
    tempVar = ""
    if tempNum in variables.keys():
        tempVar = tempNum 
        tempNum = variables[tempNum]

    tempNum = tempNum.strip()
    if ":" not in tempNum:
        tempNum = str(sci_to_float(tempNum))
        returnValue = str(tempNum)
    else:
        # This means you want range
        tempLow = max(float(sci_to_float(tempNum.split(":")[0][1:])),float(tempLow))
        tempHigh = sci_to_float(tempNum.split(":")[1][:-1])
        returnValue = str(random.uniform(float(tempLow),float(tempHigh)))
    if tempVar in variables.keys():
        variables[tempVar] = returnValue
    return returnValue

def sci_to_float(s):
    """
    Converts a string of the form 'aEb' into an int given by a*10^b
    """
    s = s.replace("e","E")
    if 'E' in s:
        s = s.split('E')
        return float(s[0]) * 10**float(s[1])
    return s

def findScaleValue(flags = {}, variables = {}):
    # used for scaling
    debugPrint(2, "Finding scaling value")
    Ne=10000
    if "-Ne" not in flags.keys():
        if "-n" in flags.keys():
            Ne=float(getUnscaledValue(variables, flags["-n"][0][1]))
    else:
        Ne = float(getUnscaledValue(variables, flags['-Ne'][0][0]))
    debugPrint(2,"Scaling factor found: {0}".format(Ne))
    return Ne


def populateFlags(variables, modelData):
    '''
    This will fill a dictionary with keys that equal the flags, and values that
    is a list of every time (in order) the flag is used
    '''
    debugPrint(2, "Starting: populateFlags ")
    flags = OrderedDict()
    orderedEvents = []
    lowTime = False
    # loops through all items in data
    for i, line in enumerate(modelData):
        lineSplit = line.split(',')

        flag = lineSplit[0]
        # if flag starts with -e it will be an event flag, thus, the order must be preserved
        if flag.startswith("-e") and "_" in flag:
            if len(lineSplit)>1:
                # striping any random whitepace
                lineSplit[1] = lineSplit[1].strip()
                if int(flag.split("_")[1]) > 1:
                    lowTime = modelData[i-1].split(',')[1]
                    if lineSplit[1] in variables:
                        lineSplit[1] = getUnscaledValue(variables, lineSplit[1], lowTime)
                else:
                    if lineSplit[1] in variables:
                        lineSplit[1] = getUnscaledValue(variables, lineSplit[1])
                if lineSplit[1] not in times and "inst" not in lineSplit[1]:
                    if lowTime:
                        lineSplit[1] = getUnscaledValue(variables, lineSplit[1], lowTime)
                    else:
                        lineSplit[1] = getUnscaledValue(variables, lineSplit[1])
                else:
                    Ne = findScaleValue(flags, variables)
                    lastTime = getUnscaledValue(variables, modelData[i-1].split(',')[1])
                    tempTime = str(float(lastTime) + 1)
                    while tempTime in times:
                        tempTime += 1
                    lineSplit[1] = tempTime
                times.append(lineSplit[1])
                flag = lineSplit[0].split("_")[0]



        if flag == "-t":
            flag.replace("Nachman","2.5e-8").replace("Other",'1.65e-8')

        if flag == "-F":
            my_file = Path(lineSplit[1:])
            if not my_file.is_file():
                raise ValueError("The file for -F is not in your file path.")

        if flag not in flags.keys():
            flags[flag] = [[x.strip() for x in lineSplit[1:] if x]]
        else:
            flags[flag].append([x.strip() for x in lineSplit[1:] if x])

        modelData[i] = ",".join(lineSplit)

    return flags

def processModelData(variables, modelData):
    """
    """
    debugPrint(2, "Starting: processModelData")
    processedData = {}
    
    flags = populateFlags(variables, modelData)

    if '-macs_file' in flags:
        macs_args = [flags['-macs_file'][0], flags['-length'][0][0], "-I", flags['-I'][0][0]]
    elif '-macsswig' in flags:
          macs_args = [flags['-macsswig'][0][0], flags['-length'][0][0], "-I", flags['-I'][0][0]]
    elif '-macs' in flags:
        macs_args = [flags['-macs'][0][0], flags['-length'][0][0], "-I", flags['-I'][0][0]]
    sizes = map(int, flags["-I"][0][1:])
    if (sys.version_info > (3, 0)):
        sizes = list(sizes)
    if '-discovery' in flags:
        for discovery_pop_str in flags["-discovery"][0]:
            discovery_pop = int(discovery_pop_str)-1
            if "True" in flags['-random_discovery'][0]:
                sizes[discovery_pop] += random.randint(2, sizes[discovery_pop])
            else:
                sizes[discovery_pop] += sizes[discovery_pop]
    total = float(sum(sizes))
    macs_args.insert(1,str(total))
    sizes_str = map(str, sizes)
    if (sys.version_info > (3, 0)):
        sizes_str = list(sizes_str)
    macs_args.extend(sizes_str)


    # seasons is all the time based events
    seasons = []

    Ne = findScaleValue(flags, variables)
    # processOrderedSeasons(flags, variables)
    debugPrint(3,"Processing flags in for macs_args")
    for flag in flags.keys():
        debugPrint(3,"  {}: {}".format(flag,flags[flag]))

        for tempLine in flags[flag]:
            try:
                # debugPrint(3,flag + ": " + str(tempLine))
                if flag == "-discovery":
                    processedData['discovery'] = [int(s.strip()) for s in tempLine if s]
                    continue
                if flag == "-sample":
                    processedData['sample'] = [int(s.strip()) for s in tempLine if s]
                    continue
                if flag == "-s":
                    processedData['seed'] = tempLine[0]
                if flag == "-daf":
                    processedData['daf'] = float(getUnscaledValue(variables, tempLine[0]))
                    continue
                if flag == "-length":
                    processedData['length'] = tempLine[0]
                    continue
                if flag == "-macs":
                    processedData['macs'] = tempLine[0]
                    continue
                if flag == "-I":
                    processedData["I"] = [int(s.strip()) for s in tempLine[1:] if s]
                    continue
                if flag == "-macsswig":
                    processedData['macsswig'] = tempLine[0]
                    continue
                if flag == "-n":
                    tmp = processedData.get('name', [])
                    tmp.append(tempLine[1])
                    processedData['name'] = tmp
                
                #----------------------- For Added Arguments from Model_CSV
                ignoredFlags = ["-germline",
                                "-array",
                                "-nonrandom_discovery",
                                "-random_discovery",
                                "-pedmap"]

                if flag in ignoredFlags:
                    continue

                if flag == "-Ne":
                    tempLine[0] = getUnscaledValue(variables, tempLine[0])
                if flag == "-em":
                    tempLine[3] = getUnscaledValue(variables, tempLine[3])
                    tempLine[3] = str(float(4*(float(tempLine[3])*Ne)))
                
                elif flag == "-eM" or flag == "-g":
                    tempLine[1] = getUnscaledValue(variables, tempLine[1])
                    tempLine[1] = str(float(4*(float(tempLine[1])*Ne)))

                elif flag == "-ema":
                    for i in range(2,len(tempLine)):
                        tempLine[i] = getUnscaledValue(variables, tempLine[i])
                        tempLine[i] = str(float(4*(float(tempLine[i])*Ne)))

                elif flag == "-eN" or flag == "-n":
                    tempLine[1] = getUnscaledValue(variables, tempLine[1])
                    tempLine[1] = str(float((float(tempLine[1])/Ne)))

                elif flag == "-en":
                    tempLine[2] = getUnscaledValue(variables, tempLine[2])
                    tempLine[2] = str(float((float(tempLine[2])/Ne)))

                elif flag == "-eg":
                    tempLine[2] = getUnscaledValue(variables, tempLine[2])
                    tempLine[2] = str(float(4*(float(tempLine[2])*Ne)))

                elif flag == "-es":
                    tempLine[2] = getUnscaledValue(variables, tempLine[2])

                elif flag == "-m":
                    tempLine[2] = getUnscaledValue(variables, tempLine[2])
                    tempLine[2] = str(float(4*(float(tempLine[2])*Ne)))

                elif flag == "-ma":
                    for i in range(len(tempLine)):
                        tempLine[i] = getUnscaledValue(variables, tempLine[i])
                        tempLine[i]=str(float(4*(float(tempLine[i])*Ne)))

                elif flag == "-t" or flag == "-r" or flag == "-G":
                    # both <m> <r> <alpha> have same scaling factor
                    tempLine[0] = getUnscaledValue(variables, tempLine[0])
                    tempLine[0] = str(float(4*(float(tempLine[0])*Ne)))

                if flag.startswith('-e'):
                    # all <t>'s are scaled
                    pass
                    tempLine[0] = getUnscaledValue(variables, tempLine[0])
                    tempLine[0]=str(round(float(tempLine[0]))/(4*Ne))
                    seasons.append([flag] + tempLine)
                else:
                    macs_args.append(flag.strip())
                    for subLine in tempLine:
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
            debugPrint(2, "discovery, sample, and daf are all missing")
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
    return processedData


def processInputFiles(paramFile, modelFile, args):
    '''
    This is the function that takes links to two files and outputs a dictionay (processedData)
    With all the (useful) data in the two files
    '''
    debugPrint(2, "Starting processInputFiles")
    
    modelData = readModelFile(modelFile)
    debugPrint(2, "Finished reading " + str(modelFile))
    debugPrint(3, "Raw input data into make_args", modelData)

    variables = readParamsFile(paramFile)
    debugPrint(2, "Finished reading " + str(paramFile))
    
    debugPrint(3,"Raw Output for variables", variables)



    processedData = processModelData(variables, modelData) # creates the input for macsSwig
    debugPrint(3,"Priting variables:", variables)

    processedData['param_dict'] = variables

    if args['genetic map']:
        processedData['macs_args'].extend(['-R', args['genetic map']])

    return processedData