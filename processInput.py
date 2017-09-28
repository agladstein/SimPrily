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
    info = {}
    for line in fl:
        if "=" in line:
            info[line.split("=")[0].strip()] = line.split("=")[1].strip()
    return info
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


def processOrderedSeasons(flags, variables):
    orderedSeasons = OrderedDict()
    debugPrint(1,"About to add time data to ordered events")

    print("="*100)
    for flag in flags.keys():

        if "_" in flag:
            # print("-{}: {}".format(flag,flags[flag]))
            # print(flag)
            if int(flag.split("_")[1]) in orderedSeasons:
                # print(flags[flag][0][0])
                if flags[flag][0][0] == 'inst':
                    orderedSeasons[int(flag.split("_")[1])][1].extend(flags.pop(flag, None))
                else:
                    for event in flags[flag]:
                        orderedSeasons[int(flag.split("_")[1])][1].insert(0,event)
                    flags.pop(flag, None)
            else:
                orderedSeasons[int(flag.split("_")[1])] = [flag,flags.pop(flag, None)]

    if not orderedSeasons:
        return orderedSeasons
    debugPrint(3,"Printing all ordered events raw data:")
    # print(orderedSeasons)
    for event in orderedSeasons:
        print("{}: {}".format(event,orderedSeasons[event]))

    print("="*100)
    for i in range(min(orderedSeasons),max(orderedSeasons)+1):
        debugPrint(2,str(i) + ": "+ str(orderedSeasons[i]))
        # looping through the flags, in order of the order tags
        if i == min(orderedSeasons):
            debugPrint(3,"first event, no change to range")
            tempLow = False
        else:
            tempLow = float(orderedSeasons[i-1][1][-1][0])
        for j in range(len(orderedSeasons[i][1])):
            if j == 0:
                # Meaning if it's the first run through of the same number
                # Find time...but also check if you need to change low
                orderedSeasons[i][1][j][0] = getUnscaledValue(variables, orderedSeasons[i][1][j][0], tempLow)
            else:
                # add a very small number
                if orderedSeasons[i][1][j][0].strip() == "inst":
                    debugPrint(3,"inst found, adding 0.00001 to " + str(float(orderedSeasons[i][1][j-1][0])))
                    orderedSeasons[i][1][j][0] = str(float(orderedSeasons[i][1][j-1][0]) + 0.00001)
                else:
                    print("Error: {0} is used before, but this time isn't set as 'inst'. Please review your input file.".format(flag) )
                    sys.exit()

    # adding keys with right time back to flags
    debugPrint(1,"Adding ordered flags back into general pool of flags")

    for flag in orderedSeasons:
        debugPrint(3,str(flag) + ": "+ str(orderedSeasons[flag]))
        tempFlag = orderedSeasons[flag][0].split("_")[0]
        if tempFlag not in flags.keys():
            flags[tempFlag] = orderedSeasons[flag][1]
        else:
            for line in orderedSeasons[flag][1]:
                flags[tempFlag].append(line)
    return orderedSeasons

def findScaleValue(flags = {}, variables = {}):
    # used for scaling
    debugPrint(1, "Finding scaling value")
    Ne=10000
    if "-Ne" not in flags.keys():
        if "-n" in flags.keys():
            Ne=float(getUnscaledValue(variables, flags["-n"][0][1]))
    else:
        Ne = float(getUnscaledValue(variables, flags['-Ne'][0][0]))
    debugPrint(2,"Scaling factor found: {0}".format(Ne))
    return Ne

def populateFlags(variables, modelData):
    debugPrint(1, "Starting: populateFlags ")
    print("="*100)
    flags = OrderedDict()
    orderedEvents = []
    lowTime = False
    for i, line in enumerate(modelData):
    # loops through all items in data
    # (data[i] = a line from input file that's has a variable)
        lineSplit = line.split(',')


            
        flag = lineSplit[0]

        if "_" in flag:
            if len(lineSplit)>1:
                lineSplit[1] = lineSplit[1].strip()
                if lineSplit[1] in variables:
                    lineSplit[1] = variables[lineSplit[1]]
                print("Before:{} ".format(i+1)+",".join(lineSplit))
                if int(flag.split("_")[1]) > 1:
                    lowTime = modelData[i-1].split(',')[1]
                if lineSplit[1] not in times and "inst" not in lineSplit[1]:
                    if lowTime:
                        lineSplit[1] = getUnscaledValue(variables, lineSplit[1], lowTime)
                    else:
                        lineSplit[1] = getUnscaledValue(variables, lineSplit[1])
                    # print("->{}".format(lineSplit[1]))
                else:
                    Ne = findScaleValue(flags, variables)
                    lastTime = getUnscaledValue(variables, modelData[i-1].split(',')[1])
                    tempTime = str(float(lastTime) + 1)
                    while tempTime in times:
                        tempTime += 1
                    print("Time '{}' has been used before: adding {} to time, changing to {}".format(lineSplit[1], str(0.00001*Ne),tempTime))
                    lineSplit[1] = tempTime
                times.append(lineSplit[1])
                flag = lineSplit[0].split("_")[0]
                print("times: {}".format(times))
                print("After:{} ".format(i+1)+",".join(lineSplit))



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

    print("="*100)
    return flags

def processModelData(variables, modelData):
    """
    """
    debugPrint(1, "Starting: processModelData")
    processedData = {}
    
    flags = populateFlags(variables, modelData)
    


    # creates a total value from the <n_n> values (from -I)
    numlist = [float(x) for x in flags['-I'][0][1:]]
    total = sum(numlist)

    
    macs_args = [flags['-macs'][0][0],str(total),flags['-length'][0][0]]

    macs_args.append("-I")
    random_discovery = True
    for tempLine in flags["-I"][0]:
        if random_discovery:
            macs_args.append(int(tempLine) + random.randint(2,int(tempLine)))
        else:
            macs_args.append(tempLine)


    # seasons is all the time based events
    seasons = []

    Ne = findScaleValue(flags, variables)
    
    # processOrderedSeasons(flags, variables)
    
    for flag in flags.keys():
        debugPrint(2,flag + ": " + str(flags[flag]))

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
                
                #----------------------- For Added Arguments from Model_CSV
                if flag == "-germline":
                    continue
                if flag == "-array":
                    continue
                if flag == "-nonrandom_discovery":
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
            except IndexError, e:
                print("There was an index error!\nThis most likely means your input file has a malformed flag.")
                print("Try running with -vv argument for last flag ran")
                sys.exit()

    if not processedData.get('discovery') or not processedData.get('sample') or not processedData.get('daf'):
        if not processedData.get('discovery') and not processedData.get('sample') and not processedData.get('daf'):
            print("discovery, sample, and daf are all missing")
        else:
            print("discovery, sample, or daf is missing")
            quit()
            

    debugPrint(1, "Adding event data back to flag pool")
    for i in range(len(seasons)):
        seasons[i][1] = float(seasons[i][1])
    seasons = sorted(seasons, key=itemgetter(1))
    for i in range(len(seasons)):
        seasons[i][1] = str(seasons[i][1])
    for season in seasons:
        macs_args.extend(season)

    processedData["macs_args"] = macs_args
    return processedData


def processInputFiles(paramFile, modelFile):
    debugPrint(1, "Starting processInputFiles")
    
    modelData = readModelFile(modelFile)
    debugPrint(1, "Finished reading " + str(modelFile))
    debugPrint(3, "Raw input data into make_args")
    for line in modelData:
        debugPrint(3,line)

    variables = readParamsFile(paramFile)
    debugPrint(1, "Finished reading " + str(paramFile))
    
    debugPrint(2,"Priting variables:")
    for var in variables:
        debugPrint(2,str(var) + ": "+ variables[var])




    processedData = processModelData(variables, modelData) # creates the input for macsSwig
    debugPrint(1, "Finished make_args()")
    debugPrint(2,"Priting variables:")
    for var in variables:
        debugPrint(2,str(var) + ": "+ variables[var])
    processedData['param_dict'] = variables



    return processedData

def main():
    # adding simply verbos flag, be sure to change
    # how you read this in later.
    if(len(sys.argv)>1):
        global verbos
        verbos = sys.argv[1].count("v")
    global variables
    
    processedData = processInputFiles("macsswig_examples/eg6/param_file_eg6.txt","macsswig_examples/eg6/model_file_eg6.csv")
    
    for data in processedData:
        print(data, processedData[data])


    # for v in processedData["variables"]:
    #     print(v, processedData["variables"][v])
        # print()
        # for d in processedData[data]:
        #     print("\t\t"+str(d))
    # print(processedData)

    # tempOutput = "Formated macs_args\n"
    # for arg in macs_args:
    #     if arg.startswith("-"):
    #         tempOutput+="\n"
    #     tempOutput+= arg + " "
    # debugPrint(2,tempOutput)

    # debugPrint(3,"Raw macs_args:\n" + str(macs_args))
    # sim = macsSwig.swigMain(len(macs_args), macs_args)
    # nbss = sim.getNumSites()
    # print(nbss)
    # return sim

if __name__ == '__main__':
    main()
